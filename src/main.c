#include <stdio.h>
#include <unistd.h>
#include "../lib/qsound.h"

int main(void) {
	if (!qsInit()) return 1;
	qsConvert("soundsReadable/sine.qsr", "sounds/sine.qs");
	qsConvert("soundsReadable/square.qsr", "sounds/square.qs");
	qsConvert("soundsReadable/sawtooth.qsr", "sounds/sawtooth.qs");
	qsConvert("soundsReadable/triangle.qsr", "sounds/triangle.qs");
	qsConvert("soundsReadable/noise.qsr", "sounds/noise.qs");

	qsConvert("soundsReadable/music.qsr", "sounds/music.qs");

	int
	sndSine = qsOpen("sounds/sine.qs"),
	sndSquare = qsOpen("sounds/square.qs"),
	sndSawtooth = qsOpen("sounds/sawtooth.qs"),
	sndTriangle = qsOpen("sounds/triangle.qs"),
	sndNoise = qsOpen("sounds/noise.qs"),
	sndFile = qsOpen("sounds/music.qs");

	printf("'sine.qs'...\n");
	qsPlay(sndSine, 255, 1);
	usleep(1500000);
	printf("'square.qs'...\n");
	qsPlay(sndSquare, 255, 1);
	usleep(1500000);
	printf("'sawtooth.qs'...\n");
	qsPlay(sndSawtooth, 255, 1);
	usleep(1500000);
	printf("'triangle.qs'...\n");
	qsPlay(sndTriangle, 255, 1);
	usleep(1500000);
	printf("'noise.qs'...\n");
	qsPlay(sndNoise, 255, 1);
	usleep(1500000);
	printf("'music.qs'...\n");
	qsPlay(sndFile, 255, 0.75f);
	usleep(13000000);

	qsClose();
	return 0;
}
