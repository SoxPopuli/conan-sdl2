from conans import ConanFile, CMake, tools


class Sdl2Conan(ConanFile):
    name = "sdl2"
    version = "2.0"
    license = "zlib"
    author = "SoxPopuli"
    url = "https://github.com/libsdl-org/SDL"
    description = ("Simple DirectMedia Layer is a cross-platform development library"
                    "designed to provide low level access to audio, keyboard, mouse, joystick,"
                    "and graphics hardware via OpenGL and Direct3D.")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/libsdl-org/SDL")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("SDL/CMakeLists.txt", "project(SDL2 C CXX)",
                  ("project(SDL2 C CXX)\n"
                   "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n"
                   "conan_basic_setup()\n"))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="SDL")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="SDL")
        cmake.install()

    def package_info(self):
        self.cpp_info.name = 'SDL2'
        self.cpp_info.includedirs = ['include', 'include/SDL2']
        self.cpp_info.libs = ["SDL2", "SDL2main"]

