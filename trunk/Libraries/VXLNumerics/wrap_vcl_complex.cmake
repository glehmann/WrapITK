WRAP_CLASS("vcl_complex" FORCE_INSTANTIATE)

  FOREACH(t F D LD)
    WRAP_TEMPLATE("${ITKM_${t}}" "${ITKT_${t}}")
  ENDFOREACH(t)

END_WRAP_CLASS()

IF(WIN32)
  SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
  WRAP_CLASS("std::_Complex_base" FORCE_INSTANTIATE)
    WRAP_TEMPLATE("F" "float, _C_float_complex")
    WRAP_TEMPLATE("D" "double, _C_double_complex")
    WRAP_TEMPLATE("LD" "long double, _C_ldouble_complex")
  END_WRAP_CLASS()
ENDIF(WIN32)
