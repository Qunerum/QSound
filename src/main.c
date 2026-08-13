#include <stdio.h>
#include <unistd.h>
#include "../lib/qsound.h"

int main(void) {
	if (!qsInit()) return 1;
	qsConvert("franxx.qsr", "franxx.qs");

	int sndFile = qsOpen("franxx.qs");

	printf("'music.qs'...\n");
	qsPlay(sndFile, 100, 0.6f);
	usleep(100000000);

	qsClose();
	return 0;
}
