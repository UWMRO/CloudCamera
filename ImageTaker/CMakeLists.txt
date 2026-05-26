cmake_minimum_required(VERSION 4.2.3)
project(ImageTaker)

add_executable(${CMAKE_PROJECT_NAME}_exe
    src/main.cpp
)


# openssag's build sucks and i don't want to deal with it so
find_package(PkgConfig REQUIRED)
pkg_check_modules(libusb REQUIRED libusb)
add_library(openssag_custom  
    ${CMAKE_CURRENT_LIST_DIR}/lib/openssag/src/openssag.cpp
    ${CMAKE_CURRENT_LIST_DIR}/lib/openssag/src/loader.cpp
)
target_include_directories(openssag_custom PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/lib/openssag/src/
)
target_compile_options(openssag_custom PRIVATE
    -w
    -Wno-narrowing
)
target_link_libraries(openssag_custom PUBLIC 
    usb
)

target_include_directories(${CMAKE_PROJECT_NAME}_exe PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/inc/
    ${CMAKE_CURRENT_LIST_DIR}/lib/openssag/src
)


target_link_libraries(${CMAKE_PROJECT_NAME}_exe PUBLIC
    openssag_custom
)