#include <stdio.h>

#include "openssag.h"
using namespace OpenSSAG;

int main()
{
        OpenSSAG::SSAG *camera = new OpenSSAG::SSAG();

        if (camera->Connect()) {
                struct raw_image *image = camera->Expose(1);
                FILE *fp = fopen("image", "w"); 
                fwrite(image->data, 1, image->width * image->height, fp);
                fclose(fp);
                camera->Disconnect();
        }
        else {
                printf("Could not find StarShoot Autoguider\n");
        }
}
