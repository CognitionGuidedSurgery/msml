
#if VTK_MAJOR_VERSION <= 5
#define __SetInput(obj, input) obj->SetInput(input)
#define __SetStencil(obj, input) obj->SetStencil(input)
#define __AddInput(obj, input) obj->AddInput(input)
#else
#define __AddInput(obj, input) obj->AddInputData(input)
#define __SetInput(obj, input) obj->SetInputData(input)
#define __SetStencil(obj, input) obj->SetStencilData(input)
#endif


