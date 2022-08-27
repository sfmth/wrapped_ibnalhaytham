import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, with_timeout, Timer
import random

clocks_per_phase = 10

# takes ~60 seconds on my PC
@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clk, 25, units="ns")
    cocotb.fork(clock.start())
    
    dut.RSTB.value = 0
    dut.power1.value = 0;
    dut.power2.value = 0;
    dut.power3.value = 0;
    dut.power4.value = 0;

    await ClockCycles(dut.clk, 8)
    dut.power1.value = 1;
    await ClockCycles(dut.clk, 8)
    dut.power2.value = 1;
    await ClockCycles(dut.clk, 8)
    dut.power3.value = 1;
    await ClockCycles(dut.clk, 8)
    dut.power4.value = 1;

    await ClockCycles(dut.clk, 80)
    dut.RSTB.value = 1

    # wait for the project to become active
    await with_timeout(RisingEdge(dut.uut.mprj.wrapped_ibnalhaytham_1.active), 3000, 'us')
    


@cocotb.test()
async def test_all(dut):
    clock = Clock(dut.clk, 25, units="ns")
    
    dut.uut.mprj.io_in.value = 0 # initialize

    cocotb.fork(clock.start())

    await Timer(10, units="us")
    
    dut.uut.mprj.io_in[11].value = 1 # set clock input

    dut.uut.mprj.io_in[12].value = 0

    dut.uut.mprj.io_in[8].value = 1 # set inst_mem mode
    dut.uut.mprj.io_in[9].value = 1
    await Timer(10, units="us")

    await with_timeout(RisingEdge(dut.uut.mprj.wrapped_ibnalhaytham_1.core1.processor_1.clk), 500, 'us')


    # wait for the reset signal - time out if necessary - should happen around 165us
    await with_timeout(RisingEdge(dut.uut.mprj.wrapped_ibnalhaytham_1.core1.processor_1.reset), 500, 'us')
    await FallingEdge(dut.uut.mprj.wrapped_ibnalhaytham_1.core1.processor_1.reset)
    await Timer(1, units="ms")





# @cocotb.test()
# async def test_all_gl(dut):
#     clock = Clock(dut.clk, 25, units="ns")
# 
#     encoder0 = Encoder(dut.clk, dut.enc0_a, dut.enc0_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
#     encoder1 = Encoder(dut.clk, dut.enc1_a, dut.enc1_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
#     encoder2 = Encoder(dut.clk, dut.enc2_a, dut.enc2_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
# 
#     cocotb.fork(clock.start())
# 
#     # wait for the reset signal - time out if necessary - should happen around 165us
#     await with_timeout(RisingEdge(dut.design_reset), 180, 'us')
#     await FallingEdge(dut.design_reset)
#     print("design reset ok")
# 
#     # pwm should all be low at start
#     assert dut.pwm0_out.value == 0
#     assert dut.pwm1_out.value == 0
#     assert dut.pwm1_out.value == 0
#     print("pwm all 0")
# 
#     # do 3 ramps for each encoder 
#     max_count = 255
#     await run_encoder_test(encoder0, None, max_count)
#     await run_encoder_test(encoder1, None, max_count)
#     await run_encoder_test(encoder2, None, max_count)
# 
#     # sync to pwm
#     await RisingEdge(dut.pwm0_out)
#     # pwm should all be on for max_count 
#     for i in range(max_count): 
#         assert dut.pwm0_out.value == 1
#         assert dut.pwm1_out.value == 1
#         assert dut.pwm2_out.value == 1
#         await ClockCycles(dut.clk, 1)
