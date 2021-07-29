from conans import ConanFile, CMake
from conans.tools import replace_in_file

class sqlpp11Conan(ConanFile):
    name = 'sqlpp11-connector-mysql'
    version = '1.1'
    license = 'BSD'
    author = 'Gennadii Marianychenko<argent.genesis@gmail.com>'
    url = 'https://github.com/ggeenn/conan-sqlpp11-connector-mysql.git'
    description = 'Conan recipie for rbock/sqlpp11-connector-mysql'
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    short_paths = True
    requires = "sqlpp11/0.59", "libmysqlclient/8.0.17", "openssl/1.1.1k"

    def source(self):
        self.run('git clone https://github.com/rbock/sqlpp11')
        self.run('git clone https://github.com/rbock/sqlpp11-connector-mysql')
        self.run('git clone https://github.com/howardhinnant/date')
        replace_in_file(
            'sqlpp11-connector-mysql/CMakeLists.txt',
            'set(CMAKE_CXX_STANDARD 11)',
            '''
set(CMAKE_CXX_STANDARD 11)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
'''
        )
        replace_in_file('sqlpp11-connector-mysql/CMakeLists.txt',
                        'add_subdirectory(tests)', '')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="sqlpp11-connector-mysql")
        cmake.build()

    def package(self):
        self.copy('*', dst='scripts', src='sqlpp11/scripts')
        self.copy('*.h', dst='include/sqlpp11', src='sqlpp11-connector-mysql/include/sqlpp11')
        self.copy('*.lib', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.a', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.so*', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.so*', dst='bin', src='sqlpp11-connector-mysql', keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ['sqlpp-mysql']