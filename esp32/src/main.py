import gc
import micropython



micropython.alloc_emergency_exception_buf(100)
gc.collect()


# HERE LAUNCH USER CODE
# import remote
# remote.main()
