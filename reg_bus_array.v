module reg_bus_array (
    input clk,
    input reset,
    input init,
    input [9:0] write_enable,
    input [159:0] data_in,
    output [159:0] reg_out,
    output [15:0] bus_out
);
    reg [15:0] registers[9:0];
    reg [3:0] bus_driver_idx;
    integer i;
    wire [15:0] bus;

    always @(*) begin
        bus_driver_idx = 0;
        for(i = 0; i < 10; i = i + 1)
            if (write_enable[i]) bus_driver_idx = i;
    end

    assign bus = registers[bus_driver_idx];

    always @(posedge clk or posedge reset) begin
        if(reset) begin
            for(i = 0; i < 10; i = i + 1)
                registers[i] <= 0;
        end else if(init) begin
            for(i = 0; i < 10; i = i + 1)
                registers[i] <= data_in[16*i +: 16];
        end else begin
            for(i = 0; i < 10; i = i + 1)
                if(write_enable[i])
                    registers[i] <= registers[i];
                else
                    registers[i] <= registers[i] + bus;
        end
    end

    reg [159:0] reg_out_r;
    always @(*) begin
        for(i = 0; i < 10; i = i + 1)
            reg_out_r[16*i +: 16] = registers[i];
    end

    assign reg_out = reg_out_r;
    assign bus_out = bus;
endmodule

