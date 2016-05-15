/**
g++ camera.cpp -lusb -lopenssag -o camera
./camera [function] [file_name] [EXP]
./camera image bias1 0
convert -size 1280x1024 -depth 8 gray:image image.jpg
**/

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "openssag.h"
#include <string.h>
// #include "fitsio.h"

using namespace OpenSSAG;
using namespace std;

char name[256];
double expose=1000;

int main(int argc, char *args[]){

  // now take the args and call some functions.  maybe add a start and exit, or something clever.
   void image(char* name, double expose, int gain);

   cout << args[1] << ' ' << args[2] << ' ' << args[3] << ' ' << args[4] << endl;
    if (strcmp(args[1],"test")==0){
        cout << "acknowledge test" << endl;
    } else if (strcmp(args[1],"image")==0){
    // file_name, exposure
        image(args[2],atof(args[3]),atof(args[4]));
    } else {
	cout << "Did not recognize command" << endl;
	}
}

void image(char *name, double expose, int gain){

  OpenSSAG::SSAG *camera = new OpenSSAG::SSAG();
  if (camera->Connect()) {
    camera->SetGain((int)gain);
    struct raw_image *image = camera->Expose(expose);
    writeImage(image, name);

    //FILE *fp = fopen(name, "w");
    //fwrite(image->data, 1, image->width * image->height, fp);
    //fclose(fp);
    camera->Disconnect();
    }
  else {
    printf("Could not find StarShoot Autoguider\n");
    }
}

int writeImage(struct image, char *name)
{

    // Create a FITS primary array containing a 2-D image
    // declare axis arrays.
    long naxis    =   2;
    long naxes[2] = { 1024, 1280 };

    // declare auto-pointer to FITS at function scope. Ensures no resources
    // leaked if something fails in dynamic allocation.
    std::auto_ptr<FITS> pFits(0);

    try
    {
        // overwrite existing file if the file already exists.

        const std::string fileName("images/"+str(name)+".fits");

        // Create a new FITS object, specifying the data type and axes for the primary
        // image. Simultaneously create the corresponding file.

        // this image is unsigned short data, demonstrating the cfitsio extension
        // to the FITS standard.

        pFits.reset( new FITS(str(name) , image , naxis , naxes ) );
    }
    catch (FITS::CantCreate)
    {
          // ... or not, as the case may be.
          return -1;
    }


/*
   try {
      // write the image to a fits file…
      fitsfile *fptr;
      fits_create_file (&fptr, "!" + name + ".fits", &status);
      fits_create_img (fptr, FLOAT_IMG,1280,1024,&status);
      // Write a keyword – its the address you pass /
      fits_update_key(fptr,TLONG,"EXPOSURE",&expose,comment,&status);
      // write an array to the image
      fits_write_img(fptr, raw_image(), 1280, 1024, pixels[0],&status);
      fits_close_file(fptr,&status);
      status = 0 ;
      }
  catch (std::string message)
}
*/
