import requests
from datetime import datetime

from models import InstagramPost


class ContentSummarizer:
    def __init__(self, model):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def summarize_single_post(self, post_content, goal=None):
        """Summarize a single post with optional goal focus
        :param post_content: the main content of the post
        :param goal: optional focus
        :return: the summary as a string
        """
        instruction = "Create a brief summary of the following post"
        if goal:
            instruction += f" with special focus on {goal}"

        prompt = f"""{instruction}.

    Post:
    ---
    {post_content}
    ---

    Your summary should be 2-3 concise sentences capturing the key points, I'm interested in only the useful information, I don't want social media tags and hashtags.
    """

        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            }
        )

        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error: {response.status_code}, {response.text}"

    def create_unified_summary_per_single_post(self, posts: list[InstagramPost], goal: str|None =None):
        """
        Process all posts and create a single unified markdown summary file
        :param posts: list of InstagramPost
        :param goal: the optional focus
        :return: the summary as a string
        """

        print(f"Creating unified summary of {len(posts)} posts...")

        # Create individual summaries first
        post_summaries = []
        for i, post in enumerate(posts):
            print(f"Processing post {i + 1}/{len(posts)}...")

            summary = self.summarize_single_post(post.caption, goal)
            post_summaries.append({
                "id": post.post_id,
                "title": f"[{i + 1} - {post.handle}]({post.url})",
                "summary": summary
            })

        print(f"Individual post summaries procecced, creating overview")

        # Create the unified markdown file
        result = ""
        # Write header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result += f"# {timestamp} - {goal.capitalize() if goal else "General"}\n\n"

        # Create an overall summary of all posts
        result += f"## Overview\n\n"
        all_content = "\n\n".join([f"Post {i + 1}: {post['summary']}" for i, post in enumerate(post_summaries)])
        overall_prompt = f"""Based on these individual post summaries, create an overview that captures the main events with dates, be concise:
    
        {all_content}
        """

        overall_response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": overall_prompt,
                "stream": False
            }
        )

        if overall_response.status_code == 200:
            overview = overall_response.json()['response']
            result += f"{overview}\n\n"
        else:
            result += "Error generating overview.\n\n"

        # Write individual post summaries
        result += f"## Post Summaries\n\n"
        for post in post_summaries:
            result += f"### {post['title']}\n"
            result += f"{post['summary']}\n\n"

        print(f"Unified summary created")
        return result

    def create_unified_summary(self, posts, goal=None):
        """
        Process all posts together and create a single unified summary

        Args:
            :param posts: List of InstagramPost
            :param goal: Optional focus/goal for the summarization

        :return the markdown summary as a string
        """
        print(f"Creating unified summary of {len(posts)} posts...")

        # Combine all posts into a single document
        xml_content = "<posts>\n"
        for i, post in enumerate(posts):
            title = f"{i} - {post.handle}"
            content = post.caption.replace('<', '&lt;').replace('>', '&gt;')  # Escape XML special chars

            xml_content += f"  <post>\n"
            xml_content += f"    <title>{title}</title>\n"
            xml_content += f"    <url>{post.url}</url>\n"
            xml_content += f"    <content>{content}</content>\n"
            xml_content += f"  </post>\n"
        xml_content += "</posts>"

        # Create the summary prompt
        instruction = "Create a comprehensive markdown summary of the following collection of posts"
        if goal:
            instruction += f" with special focus on information related to {goal}"

        prompt = f"""{instruction}.

The posts are provided in XML format below:
{xml_content}

Guidelines:
1. Create a well-structured markdown document that summarizes all the key information
2. Start with an overall summary section that captures main themes
3. If focusing on "{goal}", highlight that information prominently
4. Include a section with brief summaries of each individual post. Do not skip any post. Use as title of the post summary [title](url) as markdown link.
5. Use proper markdown formatting with headings, lists, and emphasis where appropriate
6. Ignore social media tags
"""

        # Call the API
        print("Sending request to model...")
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            }
        )

        if response.status_code == 200:
            summary = response.json()['response']

            # Add header with metadata
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"# {timestamp} - {goal.capitalize() if goal else "General"}\n\n"

            # Write to file
            result = header + summary

            print(f"Unified summary created")
            return result
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
