# User config
set ::env(DESIGN_NAME) wrapped_ibnalhaytham

# Change if needed
set ::env(VERILOG_FILES) [glob $::ibnalhaytham/src/*.v]

# Fill this
set ::env(CLOCK_PERIOD) "10.0"
#set ::env(CLOCK_NET) "clk"
set ::env(CLOCK_PORT) "clk"

set ::env(RUN_KLAYOUT_XOR) 0
set ::env(RUN_KLAYOUT_DRC) 0
set ::env(ROUTING_CORES) 8
# set ::env(DESIGN_IS_CORE) 0
set ::env(RT_MAX_LAYER) {met4}
set ::env(VDD_NETS) [list {vccd1}]
set ::env(GND_NETS) [list {vssd1}]
# don't put clock buffers on the outputs, need tristates to be the final cells
set ::env(PL_RESIZER_BUFFER_OUTPUT_PORTS) 0
#set ::env(FP_SIZING) absolute
#set ::env(DIE_AREA) "0 0 2000 2000"
set ::env(PL_TARGET_DENSITY) 0.55
set ::env(FP_CORE_UTIL) 50



set filename $::env(DESIGN_DIR)/$::env(PDK)_$::env(STD_CELL_LIBRARY)_config.tcl
if { [file exists $filename] == 1} {
	source $filename
}

