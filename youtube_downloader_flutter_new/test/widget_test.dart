import 'package:flutter_test/flutter_test.dart';
import 'package:youtube_downloader_flutter_new/main.dart';

void main() {
  testWidgets('App startet und zeigt Titel', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('YouTube Downloader'), findsOneWidget);
  });
}
