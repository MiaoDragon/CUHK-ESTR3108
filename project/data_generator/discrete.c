/**
  * This program generate discrete values from the normal distributed values
  * Arguments:
  *     [output_filename]
  * Input: normal.txt (csv, normal distribution)
  * Output: synthetic.csv (csv, discrete values)
  *                       (default filename)
  *         attributes: 0, 1, 2, 3
  *         label: 0, 1
**/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char** argv)
{
    char *out_filename = "synthetic.csv";
    char *in_filename = "normal.txt";
    if (argc > 2)
    {
        fprintf(stderr, "Wrong number of arguments!\n");
        exit(-1);
    }
    if (argc == 2)  out_filename = argv[1];
    char in_filepath[100], out_filepath[100];
    strcpy(out_filepath, "../data/");
    strcat(out_filepath, out_filename);
    strcpy(in_filepath, "../data/");
    strcat(in_filepath, in_filename);
    FILE *in = fopen(in_filepath, "r");
    FILE *out = fopen(out_filepath, "w");
    float normal;
    int discrete;
    char c;
    do
    {
        if (!fscanf(in, "%f", &normal))
            break;
        if (!fscanf(in, "%c", &c))
            break;
        if (feof(in))  break;
        if (c == '\n')      // normal is a label
        {
            discrete = (int) normal;
        }
        else                // nromal is a attribute
        {
            if (normal >= 1)            discrete = 3;
            else if (normal >= 0)       discrete = 2;
            else if (normal >= -1)      discrete = 1;
            else                        discrete = 0;
        }
        fprintf(out, "%d%c", discrete, c);
    } while (!feof(in));
    fclose(in);
    fclose(out);
}
