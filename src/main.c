#include <stdio.h>
#include <unistd.h>
#include "../lib/qsound.h"

int main(void) {
	if (!qsInit()) return 1;
	qsConvert("soundsReadable/music.qsr", "sounds/music.qs");

	int sndFile = qsOpen("sounds/music.qs");

	printf("'music.qs'...\n");
	qsPlay(sndFile, 100, 0.6f);
	usleep(13000000);

	qsClose();
	return 0;
}
