#include <string_view>
#include <string>

static constexpr std::string_view arg_format = "(type)argument should be: {test|image}command, (string)file_namepath, (double)exposure_time, (int)gain";

int image(const std::string &name, const double expose, const int gain);
