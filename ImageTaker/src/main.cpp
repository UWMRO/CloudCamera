
#include "main.hpp"

#include <iostream>

#include "openssag.h"

int main(int argc, char *args[])
{
    if (argc != 5)
    {
        std::cerr << "exactly 4 arguments must be supplied" << std::endl;
        std::cout << arg_format << std::endl;
        return 1;
    }

    if (std::string(args[1]) == "test")
    {
        std::cout << "acknowledge test" << std::endl;
        return 0;
    }
    else if (std::string(args[1]) == "image")
    {
        // file_name, exposure
        return image(args[2], atof(args[3]), atof(args[4]));
    }
    else
    {
        std::cerr << "unrecognized arg" << std::endl;
        std::cout << arg_format << std::endl;
        return 1;
    }
}

int image(const std::string &name, const double expose, const int gain)
{

    OpenSSAG::SSAG *camera = new OpenSSAG::SSAG();
    if (camera->Connect(true))
    {
        camera->SetGain((int)gain);
        struct OpenSSAG::raw_image *image = camera->Expose(expose);
        FILE *fp = fopen(name.c_str(), "w");
        fwrite(image->data, 1, image->width * image->height, fp);
        fclose(fp);
        camera->Disconnect();
        return 0;
    }
    else
    {
        std::cerr << "could not find StarShoot Autoguider" << std::endl;
        return 1;
    }
}
