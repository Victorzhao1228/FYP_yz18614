% Demo to extract frames and get frame means from a movie
% and save individual frames to separate image files.
% Then rebuilds a new movie by recalling the saved images from disk.
% Also computes the mean gray value of the color channels
% And detects the difference between a frame and the previous frame.
% Illustrates the use of the VideoReader and VideoWriter classes.

clc;    % Clear the command window.
close all;  % Close all figures (except those of imtool.)
imtool close all;  % Close all imtool figures.
clear;  % Erase all existing variables.
workspace;  % Make sure the workspace panel is showing.
fontSize = 22;

% Open the rhino.avi demo movie that ships with MATLAB.
% First get the folder that it lives in.
folder = fileparts(which('111.m4v')); % Determine where demo folder is (works with all versions).
% Pick one of the two demo movies shipped with the Image Processing Toolbox.
% Comment out the other one.
movieFullFileName = fullfile(folder,'111.m4v');
% movieFullFileName = fullfile(folder, 'traffic.avi');
% Check to see that it exists.
if ~exist(movieFullFileName, 'file')
	strErrorMessage = sprintf('File not found:\n%s\nYou can choose a new one, or cancel', movieFullFileName);
	response = questdlg(strErrorMessage, 'File not found', 'OK - choose a new movie.', 'Cancel', 'OK - choose a new movie.');
	if strcmpi(response, 'OK - choose a new movie.')
		[baseFileName, folderName, FilterIndex] = uigetfile('*.avi');
		if ~isequal(baseFileName, 0)
			movieFullFileName = fullfile(folderName, baseFileName);
		else
			return;
		end
	else
		return;
	end
end

videoObject = VideoReader(movieFullFileName);
numberOfFrames = videoObject.numberofframes;
numberOfFramesWritten = 0;  
[folder, baseFileName, extentions] = fileparts(movieFullFileName);
outputFolder = sprintf(folder, baseFileName);
if ~exist(outputFolder, 'dir')
	mkdir(outputFolder);
end
frame = 100;
thisFrame = read(videoObject, frame+1);
outputBaseFileName = sprintf('Frame_1.jpg', frame);
outputFullFileName = fullfile(outputFolder, outputBaseFileName);
imwrite(thisFrame, outputFullFileName);
