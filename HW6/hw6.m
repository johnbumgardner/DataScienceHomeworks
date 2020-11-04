% Nicholas Himes and John Bumgardner
% ECE 592
% HW 6

%% Question 1

%% Open the original mountain photo
img = imread("mountain.jpg");

%% Build compressed wtc files
wcompress('c','mountain.jpg','comp_mountain1.wtc', 'ezw');
wcompress('c','mountain.jpg','comp_mountain2.wtc', 'spiht');
wcompress('c','mountain.jpg','comp_mountain3.wtc', 'stw');
wcompress('c','mountain.jpg','comp_mountain4.wtc', 'wdr');
wcompress('c','mountain.jpg','comp_mountain5.wtc', 'aswdr');
wcompress('c','mountain.jpg','comp_mountain6.wtc', 'spiht_3d');
wcompress('c','mountain.jpg','comp_mountain7.wtc', 'lvl_mmc');
wcompress('c','mountain.jpg','comp_mountain8.wtc', 'gbl_mmc_f');
wcompress('c','mountain.jpg','comp_mountain9.wtc', 'gbl_mmc_h');

%% Uncompress the files
uncompressed_1 = wcompress('u', 'comp_mountain1.wtc');
uncompressed_2 = wcompress('u', 'comp_mountain2.wtc');
uncompressed_3 = wcompress('u', 'comp_mountain3.wtc');
uncompressed_4 = wcompress('u', 'comp_mountain4.wtc');
uncompressed_5 = wcompress('u', 'comp_mountain5.wtc');
uncompressed_6 = wcompress('u', 'comp_mountain6.wtc');
uncompressed_7 = wcompress('u', 'comp_mountain7.wtc');
uncompressed_8 = wcompress('u', 'comp_mountain8.wtc');
uncompressed_9 = wcompress('u', 'comp_mountain9.wtc');

%% Get distortion values by comparing with mountain.jpg (img)
dist1 = distortion(img, uncompressed_1);
dist2 = distortion(img, uncompressed_2);
dist3 = distortion(img, uncompressed_3);
dist4 = distortion(img, uncompressed_4);
dist5 = distortion(img, uncompressed_5);
dist6 = distortion(img, uncompressed_6);
dist7 = distortion(img, uncompressed_7);
dist8 = distortion(img, uncompressed_8);
dist9 = distortion(img, uncompressed_9);

function dist = distortion(originalImg, newImg)
    factor = 1 / (2048*2048);
    sum = 0;
    for i = 1:2048
        for j = 1:2048
            sum = sum + (originalImg(i,j) - newImg(i,j))^2;
        end
    end
    disp(sum)
    dist = factor * sum;
    
end
    

