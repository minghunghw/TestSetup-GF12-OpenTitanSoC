`timescale 1ns/100ps

module tb;

    // import tlul_pkg::*;
    // import xbar_pkg::*;

    localparam CLK_PERIOD   = 10;

    logic clk_i;
    logic rst_ni;

    // Host interfaces
    tlul_pkg::tl_h2d_t tl_if_i; 
    tlul_pkg::tl_d2h_t tl_if_o; 
    tlul_pkg::tl_h2d_t tl_lsu_i;
    tlul_pkg::tl_d2h_t tl_lsu_o;

    // Device interfaces
    tlul_pkg::tl_h2d_t tl_iccm_o;
    tlul_pkg::tl_d2h_t tl_iccm_i;
    tlul_pkg::tl_h2d_t tl_dccm_o;
    tlul_pkg::tl_d2h_t tl_dccm_i;
    tlul_pkg::tl_h2d_t tl_gpio_o;
    tlul_pkg::tl_d2h_t tl_gpio_i;
    tlul_pkg::tl_h2d_t tl_ldo1_o;
    tlul_pkg::tl_d2h_t tl_ldo1_i;
    tlul_pkg::tl_h2d_t tl_ldo2_o;
    tlul_pkg::tl_d2h_t tl_ldo2_i;
    tlul_pkg::tl_h2d_t tl_dcdc_o;
    tlul_pkg::tl_d2h_t tl_dcdc_i;
    tlul_pkg::tl_h2d_t tl_pll1_o;
    tlul_pkg::tl_d2h_t tl_pll1_i;
    tlul_pkg::tl_h2d_t tl_tsen1_o;
    tlul_pkg::tl_d2h_t tl_tsen1_i;
    tlul_pkg::tl_h2d_t tl_tsen2_o;
    tlul_pkg::tl_d2h_t tl_tsen2_i;
    tlul_pkg::tl_h2d_t tl_dap_o;
    tlul_pkg::tl_d2h_t tl_dap_i;
    tlul_pkg::tl_h2d_t tl_plic_o;
    tlul_pkg::tl_d2h_t tl_plic_i;
    tlul_pkg::tl_h2d_t tl_uart_o;
    tlul_pkg::tl_d2h_t tl_uart_i;

    xbar_periph u_xbar_periph (
        .*
    );

    initial clk_i = 0;
    initial rst_ni = 0;
    always #(CLK_PERIOD/2.0) clk_i = ~clk_i;

    initial begin
        
        tl_if_i     = tlul_pkg::TL_H2D_DEFAULT;
        tl_lsu_i    = tlul_pkg::TL_H2D_DEFAULT; 
        tl_iccm_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_dccm_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_gpio_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_ldo1_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_ldo2_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_dcdc_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_pll1_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_tsen1_i  = tlul_pkg::TL_D2H_DEFAULT;
        tl_tsen2_i  = tlul_pkg::TL_D2H_DEFAULT;
        tl_dap_i    = tlul_pkg::TL_D2H_DEFAULT;
        tl_plic_i   = tlul_pkg::TL_D2H_DEFAULT;
        tl_uart_i   = tlul_pkg::TL_D2H_DEFAULT;
        
        @(negedge clk_i)
        rst_ni      = 1;

        @(negedge clk_i)
        invoke_tempSense(tl_lsu_i);

        #200;
        if (tl_tsen1_o.a_valid) begin
            $display("%c[1;32m",27);
            $display("Success\n");
            $display("%c[0m",27);
        end else begin
            $display("%c[1;31m",27);
            $display("Failure\n");
            $display("%c[0m",27);
        end
	    $finish;
    end

endmodule

task automatic invoke_tempSense;
    output tlul_pkg::tl_h2d_t tl_lsu_i;
    tl_lsu_i.a_valid    = 1;
    tl_lsu_i.a_opcode   = tlul_pkg::tl_a_m_op'('0);
    tl_lsu_i.a_param    = 0;
    tl_lsu_i.a_size     = 0;
    tl_lsu_i.a_source   = 0;
    tl_lsu_i.a_address  = xbar_pkg::ADDR_SPACE_TSEN1;
    tl_lsu_i.a_mask     = 4'hf;
    tl_lsu_i.a_data     = 32'hffff_ffff;
    tl_lsu_i.d_ready    = 1;
endtask