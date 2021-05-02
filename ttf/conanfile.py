from conans import ConanFile, CMake, tools


class Sdl2TtfConan(ConanFile):
    name = "sdl2-ttf"
    version = "2.0.15"
    license = "zlib"
    author = "SoxPopuli"
    url = "https://github.com/libsdl-org/SDL_ttf"
    description = "Simple library to load images of various formats as SDL surfaces."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = [ "cmake_paths", "cmake_find_package" ]
    requires = [ 'sdl2/2.0', 'freetype/2.10.4' ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/libsdl-org/SDL_ttf")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("SDL_ttf/CMakeLists.txt", "project(SDL_ttf C)",
                  '''
                    project(SDL_ttf C)
                    include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
                  ''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="SDL_ttf")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="SDL_ttf")
        cmake.install()

    def package_info(self):
        self.cpp_info.name = 'SDL2_ttf'
        self.cpp_info.includedirs = ['include', 'include/SDL2']
        self.cpp_info.libs = ["SDL2_ttf"]

