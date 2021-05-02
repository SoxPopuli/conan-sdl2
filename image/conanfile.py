from conans import ConanFile, CMake, tools


class Sdl2ImageConan(ConanFile):
    name = "sdl2-image"
    version = "2.0.6"
    license = "zlib"
    author = "SoxPopuli"
    url = "https://github.com/libsdl-org/SDL_image"
    description = "Simple library to load images of various formats as SDL surfaces."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = [ "cmake_paths", "cmake_find_package" ]
    build_requires = [ 'libpng/1.6.37', 'libjpeg/9d', 'zlib/1.2.11', 'libwebp/1.2.0' ]
    requires = [ 'sdl2/2.0' ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/libsdl-org/SDL_image")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        cmakefile = "SDL_image/CMakeLists.txt"
        tools.replace_in_file(cmakefile, "project(SDL_image C)",
                  '''
                    project(SDL_image C)
                    include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
                    find_package(ZLIB REQUIRED)
                    find_package(PNG REQUIRED)
                    find_package(JPEG REQUIRED)
                    find_package(WebP REQUIRED)
                  ''')
        libraries = 'PNG::PNG JPEG::JPEG WebP::WebP'
        definitions = '-DLOAD_JPG -DLOAD_PNG -DLOAD_WEBP'
        tools.replace_in_file(cmakefile, 
                              'target_link_libraries(SDL2_image PUBLIC SDL2::SDL2-static)',
                              (f'target_link_libraries(SDL2_image PUBLIC SDL2::SDL2 PRIVATE {libraries})\n'
                               f'target_compile_definitions(SDL2_image PRIVATE {definitions})\n')
                      )
        tools.replace_in_file(cmakefile, 
                              'target_link_libraries(SDL2_image PUBLIC SDL2::SDL2)',
                              (f'target_link_libraries(SDL2_image PUBLIC SDL2::SDL2 PRIVATE {libraries})\n'
                               f'target_compile_definitions(SDL2_image PRIVATE {definitions})\n')
                      )
        tools.replace_in_file(cmakefile, 'add_library(SDL2::image ALIAS SDL2_image)',
                              '''
                              add_library(SDL2::image ALIAS SDL2_image)
                              install(
                                TARGETS SDL2_image
                                ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
                                LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
                                RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
                              )
                              install(
                                FILES SDL_image.h miniz.h nanosvg.h nanosvgrast.h 
                                DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/SDL2
                              )
                              '''

                              )

    def cmake_config(self):
        cmake = CMake(self)
        cmake.definitions['SUPPORT_PNG'] = 'OFF'
        cmake.definitions['SUPPORT_JPG'] = 'OFF'
        cmake.definitions['SUPPORT_WEBP'] = 'OFF'
        cmake.configure(source_folder="SDL_image")
        return cmake

    def build(self):
        cmake = self.cmake_config()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self.cmake_config()
        cmake.install()

    def package_info(self):
        self.cpp_info.name = 'SDL2_image'
        self.cpp_info.includedirs = ['include', 'include/SDL2']
        self.cpp_info.libs = ["SDL2_image"]

