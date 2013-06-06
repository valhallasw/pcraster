build_type="Release"
date=`date +%Y%m%d`
base_name="pcraster-${PCRTEAM_PLATFORM##*/}-$date"
build_root=`pwd`
install_prefix=`pwd`/$base_name

make_pcraster_package.sh "$build_root" "$install_prefix" $build_type
