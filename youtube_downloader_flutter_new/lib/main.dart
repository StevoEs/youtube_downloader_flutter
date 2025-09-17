import 'package:flutter/material.dart';
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
    final url = _urlController.text.trim();
    if (url.isEmpty) return;

    setState(() => _status = '⏳ Starte Download...');

    try {
      final result = await YtDlpService.runDownload(url);
      setState(() => _status = '✅ Fertig:\n$result');
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
            Expanded(
              child: SingleChildScrollView(child: Text(_status)),
            ),
          ],
        ),
      ),
    );
  }
}
