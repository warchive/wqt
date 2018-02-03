cmake_minimum_required(VERSION {{version-qt}})

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/toolchain/cmake)
include(Functions)

set(PROJECT_NAME {{name-project}})

project(${PROJECT_NAME})
set(CMAKE_CXX_STANDARD {{version-c++}})
add_definitions(-I/${CMAKE_CURRENT_SOURCE_DIR}/toolchain/helper)
add_definitions(-I/${CMAKE_CURRENT_SOURCE_DIR}/src)
add_definitions(-I/${CMAKE_CURRENT_SOURCE_DIR}/lib)

# project directories
set(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(SOURCE_DIR ${ROOT_DIR}/src)
set(BUILD_DIR ${ROOT_DIR}/build)
set(BIN_DIR ${ROOT_DIR}/bin)
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install)
set(PROJECT_INSTALL_DIR ${CMAKE_INSTALL_PREFIX})

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

# qt
set(QT_VERSION {{version-qt}})
set(QT_MODULES {{libraries-qt}})
find_package(Qt5 ${QT_VERSION} MIN CONFIG REQUIRED ${QT_MODULES})
set(CMAKE_AUTOMOC true)

# configure files
configure_file(${ROOT_DIR}/cmake/meta.hpp.in ${BUILD_DIR}/meta.hpp)

# definitions
add_definitions(${QT_DEFINITIONS})
add_definitions(-DUSE_INSTALL_TARGET)

# sources
add_sources(${SOURCE_DIR}/app app SOURCE_FILES)

# set property
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_include_directories(${PROJECT_NAME} PUBLIC ${BUILD_DIR})

# copy resources
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory "${ROOT_DIR}/res" ${BIN_DIR}/resources)
add_custom_target(CopyResources ALL COMMAND ${CMAKE_COMMAND} -E copy_directory "${ROOT_DIR}/res" ${BIN_DIR}/resources)

# link
target_link_libraries(${PROJECT_NAME} {{link-libraries}})
