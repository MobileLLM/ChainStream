package io.github.privacystreams.utils;

import android.graphics.ImageFormat;
import android.graphics.PixelFormat;
import android.media.MediaRecorder;
import android.util.Log;

/**
 * Global configurations for PrivacyStreams.
 */

public class Globals {
    public static class LocationConfig {
        public static boolean useGoogleService = true;
    }

    public static class AudioConfig {
        public static int outputFormat = MediaRecorder.OutputFormat.AMR_NB;
        public static int audioEncoder = MediaRecorder.AudioEncoder.AMR_NB;
        public static int audioSource = MediaRecorder.AudioSource.MIC;

        public static boolean useAlarmScheduler = true; // whether to use alarm manager to record periodic audio
    }

    public static class DebugConfig {
        public static int socketPort = 7336;
    }

    public static class LoggingConfig {
        public static boolean isEnabled = true;
        public static int level = Log.DEBUG;
    }

    public static class HashConfig {
        public static String defaultAlgorithm = HashUtils.SHA256;

    }

    public static class TimeConfig {
        public static String defaultTimeFormat = "yyyyMMdd_HHmmssSSS";

    }

    public static class DropboxConfig {
        public static String accessToken = "";
        public static long leastSyncInterval = 0;
        public static boolean onlyOverWifi = false;
    }

    public static class StorageConfig {
        public static String fileAppendSeparator = "\n\n\n";
    }

    public static class ImageConfig {
        public static boolean bgUseAlarmScheduler = true; // whether to use alarm manager to schedule background events
        public static int bgImageSizeLevel = 1; // size level of the image taken in background, 0 - small, 1 - medium, 2 - high
        public static long bgCameraDelay = 2000;
    }
}
