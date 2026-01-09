from lxml import etree
import html


def parser(xml_data):
    """
    Parses the XML data from the RSS feed and extracts jokes.
    Returns a list of jokes as strings.
    """
    print("Parsing XML data...")
    root = etree.fromstring(xml_data)
    jokes = []
    for item in root.findall('.//item'):
        description = item.find('description')
        if description is not None and description.text:
            text = description.text.strip().replace('<br>', '\n')
            text = html.unescape(text)
            jokes.append(text)
    print(f"Extracted {len(jokes)} jokes.")
    return jokes


if __name__ == "__main__":
    xml_data = """<rss xmlns:blogChannel="http://backend.userland.com/blogChannelModule" version="2.0">
    <channel>
    <title>Свежая десятка смешных анекдотов. Анекдоты из России.</title>
    <link>https://www.anekdot.ru/</link>
    <description>Анекдоты из России - самые смешные анекдоты, истории, афоризмы и фразы, стишки, карикатуры и другой юмор. Выходят с 8 ноября 1995 года. Составитель Дима Вернер</description>
    <language>ru</language>
    <copyright>Copyright 2026 ANEKDOT.RU</copyright>
    <managingEditor>verner@anekdot.ru (Dima Verner)</managingEditor>
    <webMaster>verner@anekdot.ru (Dima Verner)</webMaster>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <lastBuildDate>Thu, 08 Jan 2026 13:30:01 +0300</lastBuildDate>
    <image>
    ...
    </image>
    <item>
    ...
    </item>
    <item>
    ...
    </item>
    <item>
    ...
    </item>
    <item>
    <title>Анекдот №4 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571022</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ Случайно зашедшего на автобазу человека по имени Платон загрызли обезумевшие дальнобойщики... ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571022/</guid>
    <comments>https://www.anekdot.ru/id/1571022/</comments>
    </item>
    <item>
    <title>Анекдот №5 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571023</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ Никогда не верьте коммунистам, которые крестятся, депутатам, которые обещают и Гидрометцентру. ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571023/</guid>
    <comments>https://www.anekdot.ru/id/1571023/</comments>
    </item>
    <item>
    <title>Анекдот №6 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571024</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ - Ну а как организатор он как?<br>- Неповторим! Там, где спокойно поместятся четверо, он впихнёт двоих так, что им тесно будет. ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571024/</guid>
    <comments>https://www.anekdot.ru/id/1571024/</comments>
    </item>
    <item>
    <title>Анекдот №7 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571025</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ - Значитца так... Будем повышать интерес к отечественной кинопродукции и потому ее должно быть гораздо больше на экранах.<br>- А если не будут смотреть?<br>- Отключим Youtube. ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571025/</guid>
    <comments>https://www.anekdot.ru/id/1571025/</comments>
    </item>
    <item>
    <title>Анекдот №8 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571026</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ - Администрация Трампа потребовала от Венесуэлы отказаться от сотрудничества с Китаем, Россией, Ираном и Кубой и разорвать экономические связи с ними.<br>- А то что?<br>- А то они продолжат воровать людей! ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571026/</guid>
    <comments>https://www.anekdot.ru/id/1571026/</comments>
    </item>
    <item>
    <title>Анекдот №9 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571027</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ Судья - Мадуро:<br>- Осужденный, что вы можете сказать в свое оправдание?<br>Адвокат:<br>- Постойте, судебный процесс только начался! Он еще не осужденный, а обвиняемый!<br>Судья - адвокату:<br>- Учитывая, что его сюда притащили, и, особенно, как его сюда притащили - он уже осужденный... И, между прочим, это никак не зависит ни от Вас, ни от меня... имейте это в виду... ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571027/</guid>
    <comments>https://www.anekdot.ru/id/1571027/</comments>
    </item>
    <item>
    <title>Анекдот №10 за 08 января 2026</title>
    <link>https://www.anekdot.ru/release/anekdot/day/2026-01-08/#1571028</link>
    <pubDate>Thu, 08 Jan 2026 00:00:00 +0300</pubDate>
    <description>
    <![CDATA[ Трамп открыл ящик Мадуры... ]]>
    </description>
    <guid>https://www.anekdot.ru/id/1571028/</guid>
    <comments>https://www.anekdot.ru/id/1571028/</comments>
    </item>
    </channel>
    </rss>
    """
    parser(xml_data=xml_data)
