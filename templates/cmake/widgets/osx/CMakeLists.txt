cmake_minimum_required(VERSION {{version-cmake}})

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/wqt/cmake)
include(Functions)

set(PROJECT_NAME {{name-project}})

project(${PROJECT_NAME} LANGUAGES CXX)
set(CMAKE_CXX_STANDARD {{version-c++}})
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

# meta information
set(VERSION_MAJOR {{version-major-app}})
set(VERSION_MINOR {{version-minor-app}})
set(VERSION_PATCH {{version-patch-app}})
set(ORGANIZATION {{organization-app}})
set(DOMAIN {{domain-app}})
set(ICON_PATH ${ROOT_DIR}/res/icons)
set(ICON_NAME {{name-icon-executable}})

# qt related stuff
set(QT_VERSION {{version-qt}})
set(QT_MODULES {{libraries-qt}})

find_package(Qt5 ${QT_VERSION} QUIET CONFIG REQUIRED ${QT_MODULES})
set(CMAKE_AUTOMOC true)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOUIC_SEARCH_PATHS ${ROOT_DIR}/res/ui)

# definitions
add_definitions(${QT_DEFINITIONS})
add_definitions(-DUSE_INSTALL_TARGET)

# apple rpath
set(CMAKE_SKIP_BUILD_RPATH false)
set(CMAKE_BUILD_WITH_INSTALL_RPATH false)

# sources
add_sources(${SOURCE_DIR}/${PROJECT_NAME} ${PROJECT_NAME} SOURCE_FILES)

# set property
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(MACOSX_BUNDLE_BUNDLE_VERSION 1)
set(MACOSX_BUNDLE_LONG_VERSION_STRING ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})
set(MACOSX_BUNDLE_SHORT_VERSION_STRING ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})
set(MACOSX_BUNDLE_ICON_FILE ${ICON_NAME})
set(MACOSX_BUNDLE_BUNDLE_NAME ${PROJECT_NAME})
set(MACOSX_BUNDLE_RESOURCES ${BIN_DIR}/${PROJECT_NAME}.app/Contents/Resources)
set(MACOSX_BUNDLE_ICON ${ICON_PATH}/${MACOSX_BUNDLE_ICON_FILE})

# configure files
configure_file(${ROOT_DIR}/wqt/cmake/meta.hpp.in ${BUILD_DIR}/meta.hpp)
configure_file(${ROOT_DIR}/wqt/cmake/info.plist.in ${BUILD_DIR}/info.plist)

add_executable(${PROJECT_NAME} MACOSX_BUNDLE ${SOURCE_FILES} ${MACOSX_BUNDLE_ICON})
set_target_properties(${PROJECT_NAME} PROPERTIES MACOSX_BUNDLE_INFO_PLIST ${BUILD_DIR}/info.plist)
target_include_directories(${PROJECT_NAME} PUBLIC ${BUILD_DIR})

# copy resources
execute_process(COMMAND ${CMAKE_COMMAND} -E make_directory ${MACOSX_BUNDLE_RESOURCES})
execute_process(COMMAND ${CMAKE_COMMAND} -E copy_if_different ${MACOSX_BUNDLE_ICON} ${MACOSX_BUNDLE_RESOURCES})
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory "${ROOT_DIR}/res"
        ${BIN_DIR}/${PROJECT_NAME}.app/Contents/resources)

# link
target_link_libraries(${PROJECT_NAME} {{link-libraries}})
