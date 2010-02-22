WRAP_CLASS("itk::SubtractConstantFromImageFilter" POINTER_WITH_SUPERCLASS)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_SCALAR})
      WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_D}${ITKM_I${t}${d}}" "${ITKT_I${t}${d}},${ITKT_D},${ITKT_I${t}${d}}")
    ENDFOREACH(t)
    FOREACH(t ${WRAP_ITK_COMPLEX_REAL})
      # WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_D}${ITKM_I${t}${d}}" "${ITKT_I${t}${d}},${ITKT_D},${ITKT_I${t}${d}}")
      WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_${t}}${ITKM_I${t}${d}}" "${ITKT_I${t}${d}},${ITKT_${t}},${ITKT_I${t}${d}}")
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()
