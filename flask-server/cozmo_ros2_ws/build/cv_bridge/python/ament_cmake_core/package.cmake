set(_AMENT_PACKAGE_NAME "cv_bridge")
set(cv_bridge_VERSION "2.1.3")
set(cv_bridge_MAINTAINER "Ethan Gao <ethan.gao@linux.intel.com>")
set(cv_bridge_BUILD_DEPENDS "boost" "libopencv-dev" "python3-numpy" "sensor_msgs")
set(cv_bridge_BUILDTOOL_DEPENDS "ament_cmake_ros" "python_cmake_module")
set(cv_bridge_BUILD_EXPORT_DEPENDS "boost" "libopencv-dev" "python3-numpy" "sensor_msgs")
set(cv_bridge_BUILDTOOL_EXPORT_DEPENDS )
set(cv_bridge_EXEC_DEPENDS "ament_index_python" "boost" "libopencv-dev" "python3-numpy" "sensor_msgs")
set(cv_bridge_TEST_DEPENDS "ament_cmake_gtest" "ament_cmake_pytest" "ament_lint_auto" "ament_lint_common" "python3-opencv")
set(cv_bridge_GROUP_DEPENDS )
set(cv_bridge_MEMBER_OF_GROUPS )
set(cv_bridge_DEPRECATED "")
set(cv_bridge_EXPORT_TAGS)
list(APPEND cv_bridge_EXPORT_TAGS "<rosdoc config=\"rosdoc.yaml\"/>")
list(APPEND cv_bridge_EXPORT_TAGS "<build_type>ament_cmake</build_type>")
