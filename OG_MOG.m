foregroundDetector = vision.ForegroundDetector('NumGaussians', 3, ...
    'NumTrainingFrames', 50);

videoReader = vision.VideoFileReader('Static_cam_vid.mp4');
for i = 1:10
    frame = step(videoReader); % read the next video frame
    foreground = step(foregroundDetector, frame);
end

se = strel('square', 3);
filteredForeground = imopen(foreground, se);
%figure; imshow(filteredForeground); title('Clean Foreground');

blobAnalysis = vision.BlobAnalysis('BoundingBoxOutputPort', true, ...
    'AreaOutputPort', false, 'CentroidOutputPort', false, ...
    'MinimumBlobArea', 150);
bbox = step(blobAnalysis, filteredForeground);

savefile = 'output_OG_MOG.avi';
outputVideo = VideoWriter(fullfile('./', savefile));
%outputVideo = vision.VideoFileWriter(savefile);
outputVideo.FrameRate = 24;
%outputVideo.FrameRate = 24;
open(outputVideo);

result = insertShape(frame, 'Rectangle', bbox, 'Color', 'green');

numCars = size(bbox, 1);
result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
    'FontSize', 14);
figure; imshow(result); title('Detected Cars');

videoPlayer = vision.VideoPlayer('Name', 'Detected Cars');
videoPlayer.Position(3:4) = [650,400];  % window size: [width, height]
se = strel('square', 3); % morphological filter for noise removal

while ~isDone(videoReader)

    frame = step(videoReader); % read the next video frame
    %frame = insertShape(frame, 'Line', [161 11 233 121], 'Color', 'green');
    %frame = insertShape(frame, 'Line', [264 137 441 262], 'Color', 'red');
    % Detect the foreground in the current video frame
    foreground = step(foregroundDetector, frame);
    
    % Use morphological opening to remove noise in the foreground
    filteredForeground = imopen(foreground, se);

    % Detect the connected components with the specified minimum area, and
    % compute their bounding boxes
    %bbox = step(blobAnalysis, filteredForeground);
    %[sx sy] = size(bbox);
    %for i=1:sx
    %   if (bbox(i, 3)>30) || (bbox(i, 4)>20)
    %       % Draw bounding boxes around the detected cars
    %       result = insertShape(frame, 'Rectangle', bbox(i, :), 'Color', 'green');
    %   end
    %end
    
    
    

    % Display the number of cars found in the video frame
    %numCars = size(bbox, 1);
    %result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
    %    'FontSize', 14);
    disp = frame.*filteredForeground;
    step(videoPlayer, disp);% display the results
    writeVideo(outputVideo, disp);
end

close(outputVideo);
release(videoReader); % close the video file