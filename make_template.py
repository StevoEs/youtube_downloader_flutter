import os, zipfile

files = {
    "pubspec.yaml": """name: youtube_downloader_flutter
description: YouTube Downloader mit Flutter
publish_to: 'none'

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
""",

    "lib/main.dart": """import 'package:flutter/material.dart';
import 'yt_dlp_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'YouTube Downloader',
      theme: ThemeData(primarySwatch: Colors.red),
      home: const DownloaderPage(),
    );
  }
}

class DownloaderPage extends StatefulWidget {
  const DownloaderPage({super.key});

  @override
  State<DownloaderPage> createState() => _DownloaderPageState();
}

class _DownloaderPageState extends State<DownloaderPage> {
  final _urlController = TextEditingController();
  String _status = '';

  Future<void> _download() async {
    final url = _urlController.text;
    if (url.isEmpty) return;
    setState(() => _status = 'Starte Download...');

    try {
      final result = await YtDlpService.runDownload(url);
      setState(() => _status = '✅ Fertig:\\n$result');
    } catch (e) {
      setState(() => _status = '❌ Fehler: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('YouTube Downloader')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _urlController,
              decoration: const InputDecoration(
                labelText: 'YouTube URL eingeben',
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _download,
              child: const Text('Download starten'),
            ),
            const SizedBox(height: 20),
            Expanded(child: SingleChildScrollView(child: Text(_status))),
          ],
        ),
      ),
    );
  }
}
""",

    "lib/yt_dlp_service.dart": """import 'dart:io';

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
""",

    ".github/workflows/build-apk.yml": """name: Build Flutter APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Install Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.27.0'

      - name: Get dependencies
        run: flutter pub get

      - name: Build APK (release)
        run: flutter build apk --release

      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
        with:
          name: release-apk
          path: build/app/outputs/flutter-apk/app-release.apk
"""
}

# ZIP erstellen
zip_name = "youtube_downloader_template.zip"
with zipfile.ZipFile(zip_name, "w") as zf:
    for path, content in files.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        zf.write(path)

print(f"✅ Template erstellt: {zip_name}")
