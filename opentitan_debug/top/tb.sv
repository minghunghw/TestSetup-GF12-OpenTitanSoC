`timescale 1ns/100ps

module tb;

    localparam CLK_PERIOD   = 10;
    localparam DATA_WIDTH   = 32;

    logic clk_i;
    logic rst_ni;
    logic en_i;

    logic sel;
    logic spi_ss;
    logic spi_mosi;

    logic uart_rx_inst;
    logic uart_txen;
    logic uart_tx;
    logic uart_rx;

    logic tempsense_clkref;
    logic tempsense_clkout;

    logic [7:0] gpio_o;

    opentitan_soc_top #(
        .DATA_WIDTH (DATA_WIDTH)
    ) u_opentitan_soc_top (
        .*
    );

    initial clk_i = 0;
    initial rst_ni = 0;
    always #(CLK_PERIOD/2.0) clk_i = ~clk_i;

    initial begin
        
        en_i                = 0;
        tempsense_clkref    = clk_i;
        spi_ss              = 1;
        spi_mosi            = 0;
        sel                 = 0;
        uart_rx_inst        = 0;
        uart_rx             = 0;
        
        @(negedge clk_i)
        rst_ni      = 1;

        @(negedge clk_i)
        // $readmemh("../program/hex/test_add.hex", );

        #200;
        if (1) begin
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

task automatic hex_to_spi;
    
endtask

task automatic spi_loop;
    
endtask