import 'dart:io';

class YtDlpService {
  static Future<String> runDownload(String url) async {
    try {
      final result = await Process.run('yt-dlp', ['-F', url]);
      if (result.exitCode != 0) {
        throw Exception(result.stderr);
      }
      return result.stdout.toString();
    } catch (e) {
      throw Exception('yt-dlp nicht gefunden oder Fehler: $e');
    }
  }
}
