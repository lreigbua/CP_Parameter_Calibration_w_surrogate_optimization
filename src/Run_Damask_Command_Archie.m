function [] = Run_Damask_Command_Archie(command)
%Runs command given in command using Archie's Neper

text=fileread('../src/Run_Damask.sh');

newtext = strrep(text,'substitute',command);

writelines(newtext,'Run_Damask_Mod.sh');

status = system('sbatch -W Run_Damask_Mod.sh');
end

