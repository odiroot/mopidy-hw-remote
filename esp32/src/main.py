import gc
import micropython

import remote


micropython.alloc_emergency_exception_buf(100)
gc.collect()


# HERE LAUNCH USER CODE
remote.main()
