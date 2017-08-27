/**
 *  this program will generate a 1000*1001 samples, with n correlated features
 *  each sample has 1000 features with 1 label
 *  n (< 10) of the features are correlated
 *  features follow normal(0,1) distribution
 *  parameter:
 *      n         - number of attributes
 *      m         - number of data samples
 *          ------------------------------------------------------------
 *          file description:
 *                  first line:  n  - number of correlated numbers
 *                  second line: n sorted numbers  - index of correlated number, start from 1
 *                  n*n lines:   matrix of convariance
 *          ------------------------------------------------------------
**/
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <math.h>
#include <string.h>

static int FEATURE, SAMPLE;
int n, count;   //count for random seed
int *r_v;
int **cov;
float **A;
float **ans;
//float ans[SAMPLE][FEATURE+1];
float *z;
//functions
void read_parameter(FILE *);
float** decomp();
void normal_generate(float**, int);
void generate();
void output(FILE*);

int main(int argc, char* argv[])
{
/**
  *  1. read the parameter file
  *  2. generate A, such that AAT = covariance matrix
  *  3. generate z, an array of n independent normal random variables
  *  4. x = Az
  *  5. output x in a file
**/
    //read from file
    char *in_filename = "model.txt";
    char *out_filename = "normal.txt";
    char in_filepath[100], out_filepath[100];
    strcpy(in_filepath, "../data/");
    strcat(in_filepath, in_filename);
    strcpy(out_filepath, "../data/");
    strcat(out_filepath, out_filename);
    FILE *fr = fopen(in_filepath, "r");
    if (fr == NULL)
    {
        fprintf(stderr, "error occurred!\n");
        exit(-1);
    }
    read_parameter(fr);
    fclose(fr);
    count = 0;
    
    //generate A
    A = decomp();
    //generate samples
    z = malloc(sizeof(float) * n);
    generate();

    //output the ans into a file
    FILE *fw = fopen(out_filepath, "w");
    output(fw);
    fclose(fw);
    return 0;
}

void read_parameter(FILE *rd)
{
    fscanf(rd, "%d %d\n", &SAMPLE, &FEATURE);
    n = fgetc(rd) - '0';
    r_v = (int*) malloc(sizeof(int) * n);
    cov = (int**) malloc(sizeof(int*) * n);
    int i = 0;
    
    ans = (float**) malloc(sizeof(float*) * SAMPLE);
    for (i = 0; i < SAMPLE; i++)
        ans[i] = (float*) malloc(sizeof(float) * (FEATURE + 1));
    for (i = 0; i < n; i++)
        cov[i] = (int*) malloc(sizeof(int) * n);
    fgetc(rd);  // read \n
    char buf[255];
    fgets(buf, 254, rd);
    char *ptr = buf;
    i = 0;
    //read array
    //convert string to int
    //while (*ptr != '\0')
    while (i < n)   //note here that fgets will store '\n' inside buf
    {
        r_v[i] = (int) strtol(ptr, &ptr, 10);
        i++;
    }
    int j = 0;
    //read matrix
    for (i = 0; i < n; i++)
    {
       fgets(buf, 254, rd);
       ptr = buf;
       j = 0;
       //convert string to float
       while (j < n)
       {
            cov[i][j] = strtof(ptr, &ptr);
            j++;
       }
    }

}

float** decomp()
{
    float **A = malloc(sizeof(float*) * n);
    int i = 0, j = 0;
    for (i = 0; i < n; i++)
    {
        A[i] = malloc(sizeof(float) * n);
        for (j = i+1; j < n; j++)
            A[i][j] = 0;
    }
    //start decomposition method
    for (j = 0; j < n; j++)
    {
        //handle A[j,j] 
        //constraint:  A[j,j]^2 + sigma(k=0 to j-1, A[j,k]^2) = cov[j,j]
        float sum = 0;
        int k = 0;
        for (k = 0; k <= j-1; k++)
            sum = sum + A[j][k] * A[j][k];
        A[j][j] = cov[j][j] - sum;

        //handle A[i,j]  (i > j)
        //constraint: A[j,j]A[i,j] + sigma(k=0 to j-1, A[i,k]*A[j,k]) = cov[i,j]
        for (i = j + 1; i < n; i++)
        {
            float sum = 0;
            int k = 0;
            for (k = 0; k <= j-1; k++)
                sum = sum + A[i][k] * A[j][k];
            A[i][j] = (cov[i][j] - sum) / A[j][j];
        }
    }
    return A;
}
void generate()
{
    int i = 0, j = 0, k = 0;
    float sum;
    float *ran_v = malloc(sizeof(float) * (FEATURE-n));
    float x[n];  //normal distributed variables that follow the convariance
    for (i = 0; i < SAMPLE; i++)
    {
        //generate n independent normal distributed variables
        //use Box-Muller Transform
        normal_generate(&z, n);
        //generate other independent normal variables
        normal_generate(&ran_v, FEATURE-n);
        //get the correlated normal distributed variables from the independent ones

        for (j = 0; j < n; j++)
        {
            sum = 0;
            for (k = 0; k < n; k++)
                sum += A[j][k] * z[k];
            x[j] = sum;
        }

        //fit the correlated n variables
        for (j = 0; j < n; j++)
            ans[i][r_v[j]] = x[j];    //r_v[] is index starting from 0

        //fit the independent variables
        //suppose r_v[] is already sorted
        j = 0;
        for (k = 0; k < FEATURE; k++)
        {
            if ((j < n) && (r_v[j] == k)){     //k feature is a related variable
                j++;
                continue;
            }
        
            ans[i][k] = ran_v[k-j];     //already examined k features and j related features
            
        }

        //get label value
        //label = sign(sigma(n variable values))
        sum = 0;
        for (j = 0; j < n; j++)
            sum += x[j];
        if (sum > 0)    ans[i][FEATURE] = 1;
        else            ans[i][FEATURE] = 0;
    }

    free(ran_v);
}
void normal_generate(float **z, int n)
{
//use Box-Muller Transform
//2 uniform variables for 2 normal distributed variables
    float u1, u2, z1, z2;
    int m = 0;
    int i = 0;
    for (i = 0; i < n / 2; i++)
    {
        count++;
        srand(count*time(NULL));
        u1 = (float)rand() / (float)RAND_MAX;
        count++;
        srand(count*time(NULL));
        u2 = (float)rand() / (float)RAND_MAX;
        z1 = (float) (sqrt(-2 * log(u1)) * cos(2*M_PI*u2));
        z2 = (float) (sqrt(-2 * log(u1)) * sin(2*M_PI*u2));
        (*z)[i * 2] = z1;
        (*z)[i * 2 + 1] = z2;
        
    }
    if ((n & 1) == 1)  //n is odd
    {
        count++;
        srand(count*time(NULL));
        u1 = (float)rand() / (float)RAND_MAX;
        count++;
        srand(count*time(NULL));
        u2 = (float)rand() / (float)RAND_MAX;
        z1 = (float) (sqrt(-2 * log(u1)) * cos(2*M_PI*u2));
        (*z)[n - 1] = z1;
    }
}
void output(FILE *fw)
{
    //Convert ans[][] into CSV
    int i, j;
    for (i = 0; i < SAMPLE; i++)
    {
        fprintf(fw, "%.6f", ans[i][0]);
        for (j = 1; j < FEATURE; j++)
            fprintf(fw, ",%.6f", ans[i][j]);
        fprintf(fw, ",%.0f", ans[i][FEATURE]);
        fputc('\n', fw);
    }
}
