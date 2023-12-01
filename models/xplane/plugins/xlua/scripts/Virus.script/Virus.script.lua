--[[
*****************************************************************************************
* Program Script Name	:	Pipistrel Virus
*
* Author Name			:	Patrick Le Luyer
*
*   Revisions:
*   -- DATE --	--- REV NO ---		--- DESCRIPTION ---
* 
*
*
*
*
*****************************************************************************************
*        COPYRIGHT � 2021 Patrick Le Luyer oldpat.e-monsite.com - ALL RIGHTS RESERVED
*****************************************************************************************
--]]



--*************************************************************************************--
--** 					              XLUA GLOBALS              				     **--
--*************************************************************************************--

--[[

SIM_PERIOD - this contains the duration of the current frame in seconds (so it is alway a
fraction).  Use this to normalize rates,  e.g. to add 3 units of fuel per second in a
per-frame callback you’d do fuel = fuel + 3 * SIM_PERIOD.

IN_REPLAY - evaluates to 0 if replay is off, 1 if replay mode is on

--]]


--*************************************************************************************--
--** 					               CONSTANTS                    				 **--
--*************************************************************************************--



--*************************************************************************************--
--** 					            GLOBAL VARIABLES                				 **--
--*************************************************************************************--



--*************************************************************************************--
--** 					            LOCAL VARIABLES                 				 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				             FIND X-PLANE DATAREFS            			    	 **--
--*************************************************************************************--


simDR_ignition_system				= find_dataref("sim/cockpit2/engine/actuators/ignition_on[0]")

simDR_startup_running             	= find_dataref("sim/operation/prefs/startup_running")

simDR_battery						= find_dataref("sim/cockpit2/electrical/battery_on[0]")
simDR_generator						= find_dataref("sim/cockpit2/electrical/generator_on[0]")
simDR_fuel_pump						= find_dataref("sim/cockpit2/engine/actuators/fuel_pump_on[0]")

simDR_gear_steer					= find_dataref("sim/flightmodel2/gear/tire_steer_command_deg[0]")
simDR_rudder						= find_dataref("sim/flightmodel2/wing/rudder1_deg[10]")

--*************************************************************************************--
--** 				               FIND X-PLANE COMMANDS                   	    	 **--
--*************************************************************************************--


--*************************************************************************************--
--** 				              FIND CUSTOM DATAREFS             			    	 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				              FIND CUSTOM COMMANDS              			     **--
--*************************************************************************************--



--*************************************************************************************--
--** 				        CREATE READ-ONLY CUSTOM DATAREFS               	         **--
--*************************************************************************************--


VirusDR_switch_magneto1_position		= create_dataref("custom/virus/switch/magneto1", "number")
VirusDR_switch_magneto2_position		= create_dataref("custom/virus/switch/magneto2", "number")

VirusDR_switch_master				= create_dataref("custom/virus/switch/master", "number")

VirusDR_ignition_pos					= create_dataref("custom/virus/position/ignition", "number")

VirusDR_tiny_tach_mode				= create_dataref("custom/virus/tiny_tach_mode", "number")


--*************************************************************************************--
--** 				       READ-WRITE CUSTOM DATAREF HANDLERS     	        	     **--
--*************************************************************************************--



--*************************************************************************************--
--** 				       CREATE READ-WRITE CUSTOM DATAREFS                         **--
--*************************************************************************************--


--*************************************************************************************--
--** 				             CUSTOM COMMAND HANDLERS            			     **--
--*************************************************************************************--


function Virus_mag1_up_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_magneto1_position == 0 then
			VirusDR_switch_magneto1_position = 1
		end
	end
end

function Virus_mag1_dn_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_magneto1_position == 1 then
			VirusDR_switch_magneto1_position = 0
		end
	end
end

function Virus_mag2_up_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_magneto2_position == 0 then
			VirusDR_switch_magneto2_position = 1
		end
	end
end

function Virus_mag2_dn_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_magneto2_position == 1 then
			VirusDR_switch_magneto2_position = 0
		end
	end
end


function Virus_master_on_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_master == 0 then
			VirusDR_switch_master = 1
		end
	end
end

function Virus_master_off_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_switch_master == 1 then
			VirusDR_switch_master = 0
		end
	end
end

function Virus_tiny_tach_mode_CMDhandler(phase, duration)
	if phase == 0 then
		if VirusDR_tiny_tach_mode == 0 then
			VirusDR_tiny_tach_mode = 1
		elseif VirusDR_tiny_tach_mode == 1 then
			VirusDR_tiny_tach_mode = 2
		elseif VirusDR_tiny_tach_mode == 2 then
			VirusDR_tiny_tach_mode = 0
		end
	end
end

--*************************************************************************************--
--** 				              CREATE CUSTOM COMMANDS              			     **--
--*************************************************************************************--

VirusCMD_mag1_up						= create_command("custom/virus/switch/magneto1_up", "Magneto 1 On", Virus_mag1_up_CMDhandler)
VirusCMD_mag1_dn						= create_command("custom/virus/switch/magneto1_dn", "Magneto 1 Off", Virus_mag1_dn_CMDhandler)

VirusCMD_mag2_up						= create_command("custom/virus/switch/magneto2_up", "Magneto 2 On", Virus_mag2_up_CMDhandler)
VirusCMD_mag2_dn						= create_command("custom/virus/switch/magneto2_dn", "Magneto 2 Off", Virus_mag2_dn_CMDhandler)

VirusCMD_master_on					= create_command("custom/virus/switch/master_on", "Master Switch On", Virus_master_on_CMDhandler)
VirusCMD_master_off					= create_command("custom/virus/switch/master_off", "Master Switch Off", Virus_master_off_CMDhandler)

VirusCMD_tiny_tach_mode				= create_command("custom/virus/button/tiny_tack_mode", "Tiny Tach Mode Cycle", Virus_tiny_tach_mode_CMDhandler)

--*************************************************************************************--
--** 				             X-PLANE COMMAND HANDLERS               	    	 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				             REPLACE X-PLANE COMMANDS                  	    	 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				              WRAP X-PLANE COMMANDS                  	    	 **--
--*************************************************************************************--



--*************************************************************************************--
--** 					           OBJECT CONSTRUCTORS         		        		 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				                  CREATE OBJECTS              	     			 **--
--*************************************************************************************--



--*************************************************************************************--
--** 				                 SYSTEM FUNCTIONS           	    			 **--
--*************************************************************************************--

function Virus_magneto_switches()


	if VirusDR_switch_magneto1_position == 0 then
		if VirusDR_switch_magneto2_position == 0 then
			VirusDR_ignition_pos = 0
		elseif VirusDR_switch_magneto2_position == 1 then
			VirusDR_ignition_pos = 2
		end
	elseif VirusDR_switch_magneto1_position == 1 then
		if VirusDR_switch_magneto2_position == 0 then
			VirusDR_ignition_pos = 1
		elseif VirusDR_switch_magneto2_position == 1 then
			VirusDR_ignition_pos = 3
		end
	end


	simDR_ignition_system = VirusDR_ignition_pos


end






function Virus_master_switch()

	if VirusDR_switch_master == 0 then
		simDR_battery = 0
		simDR_generator = 0
		simDR_fuel_pump = 0
	elseif VirusDR_switch_master == 1 then
		simDR_battery = 1
		simDR_generator = 1
		simDR_fuel_pump = 1
	end

end

----- FLIGHT START ---------------------------------------------------------------------
function Virus_flight_start_systems()

    -- ALL MODES ------------------------------------------------------------------------
    
    
    


    -- COLD & DARK ----------------------------------------------------------------------
    if simDR_startup_running == 0 then

 	VirusDR_switch_magneto1_position = 0
 	VirusDR_switch_magneto2_position = 0
	VirusDR_switch_master = 0 


    -- ENGINES RUNNING ------------------------------------------------------------------
    elseif simDR_startup_running == 1 then

	VirusDR_switch_magneto1_position = 1
	VirusDR_switch_magneto2_position = 1
	VirusDR_switch_master = 1		

    end

end



--*************************************************************************************--
--** 				               XLUA EVENT CALLBACKS       	        			 **--
--*************************************************************************************--





function flight_start()

	Virus_flight_start_systems()

end

--function flight_crash() end

function before_physics()
	
	Virus_master_switch()	
	
end

function after_physics()

	Virus_magneto_switches()

end

--function after_replay() end




--*************************************************************************************--
--** 				               SUB-MODULE PROCESSING       	        			 **--
--*************************************************************************************--

-- dofile("")



