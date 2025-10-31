from src.bk import BlastForum
import json

if __name__ == '__main__':
    msg = {}
    bk: BlastForum = BlastForum();
    response = bk.go_to();
    contents = bk.extract_text(response);
    forum_link = bk.get_heading_link('Новости', contents);
    forum_page = bk.go_to(forum_link[0]);
    forum_page_content = bk.extract_text(forum_page);
    topic_links = bk.get_topic_links(forum_page_content);
    topic_titles = bk.get_article_title(forum_page_content);
    topic_reference = {k: topic_titles[k-1] for k in range(1, len(topic_titles)+1)}

    for index in range(1, len(topic_links) + 1):

        topic_response = bk.go_to(topic_links[index-1])
        topic_content = bk.extract_text(topic_response)
        topic_last_page_link = bk.get_last_page_link(topic_links[index-1],topic_content)
        if topic_last_page_link:
            topic_last_page_response = bk.go_to(topic_last_page_link[0])
            topic_content = bk.extract_text(topic_last_page_response)
        articles = bk.get_articles(topic_content)

        art = ''
        for article in articles:
            art = art + '\n' + article;
        art = bk.remove_quotes(art);

        messages =bk.get_messages_with_no_quotes(art)
        authors = bk.get_author_and_time(art)
        topics = []
        for i in range(len(messages) - 1):
            author = authors[i].split('&middot;')
            words_count = bk.get_words(messages[i])
            tmp = {'message': messages[i], 'author': author[0],'date_time': author[1], 'words_count': len(words_count)}
            topics.append(tmp)
        msg[topic_reference[index]] = topics

    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(msg, indent=4, ensure_ascii=False))

