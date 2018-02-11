cmake_minimum_required(VERSION {{version.cmake}})

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/wqt/cmake)
include(Functions)

set(PROJECT_NAME {{project.name}})

project(${PROJECT_NAME} LANGUAGES CXX)
set(CMAKE_CXX_STANDARD {{version.cxx}})
add_definitions(-I/${CMAKE_CURRENT_SOURCE_DIR}/src)
add_definitions(-I/${CMAKE_CURRENT_SOURCE_DIR}/lib)

# project directories
set(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(SOURCE_DIR ${ROOT_DIR}/src)
set(BUILD_DIR ${ROOT_DIR}/wqt/build)
set(BIN_DIR ${ROOT_DIR}/bin)

# output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${BIN_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${BIN_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${BIN_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${BIN_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${BIN_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${BIN_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${BIN_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${BIN_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${BIN_DIR})

# qt related stuff
set(QT_VERSION {{version.qt}})
set(QT_MODULES {{library.qt}})

find_package(Qt5 ${QT_VERSION} QUIET CONFIG REQUIRED ${QT_MODULES})
set(CMAKE_AUTOMOC true)

# definitions
add_definitions(${QT_DEFINITIONS})
add_definitions(-DUSE_INSTALL_TARGET)

# sources
add_sources(${SOURCE_DIR}/${PROJECT_NAME} ${PROJECT_NAME} SOURCE_FILES)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_include_directories(${PROJECT_NAME} PUBLIC ${BUILD_DIR})

# link
target_link_libraries(${PROJECT_NAME} {{library.link}})
