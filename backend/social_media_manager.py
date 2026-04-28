"""
Autonomous Social Media Manager Multi-Agent System
=================================================
This system automates social media content creation with multiple agents:
- Trend Monitor: Identifies trending topics
- Content Creator: Writes engaging captions
- Image Describer: Describes images to create (simulated)
- Brand Guardian: Ensures brand consistency
- Scheduler: Determines optimal posting time
"""

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from colorama import Fore
from datetime import datetime, timedelta
import config
from utils import print_agent_message, print_section


class TrendMonitorAgent:
    """Monitors and identifies trending topics."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_CREATIVE
        )
        
        self.prompt = PromptTemplate(
            input_variables=["industry", "current_date"],
            template="""You are a Social Media Trend Analyst.

Industry: {industry}
Date: {current_date}

Identify 3 trending topics or themes that would be relevant for this industry right now. Consider:
- Seasonal events
- Industry news
- Popular culture
- Hashtag trends

For each trend, provide:
1. Topic name
2. Why it's trending
3. Relevance score (1-10)

Format as a numbered list."""
        )
        
        self.chain = self.prompt | self.llm
    
    def find_trends(self, industry: str) -> str:
        """Identify trending topics for an industry."""
        print_agent_message("Trend Monitor Agent", f"Analyzing trends for {industry}...", Fore.MAGENTA)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        trends = self.chain.invoke({"industry": industry, "current_date": current_date})
        
        print_agent_message("Trend Monitor Agent", f"Trending topics:\n{trends}", Fore.MAGENTA)
        return trends


class ContentCreatorAgent:
    """Creates engaging social media captions."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_CREATIVE
        )
        
        self.prompt = PromptTemplate(
            input_variables=["trend", "brand_voice", "platform", "feedback"],
            template="""You are a Social Media Content Creator.

Trend/Topic: {trend}
Brand Voice: {brand_voice}
Platform: {platform}
{feedback}

Create an engaging social media post that:
1. Hooks attention in the first line
2. Relates to the trend
3. Matches the brand voice
4. Includes 3-5 relevant hashtags
5. Has a call-to-action

Keep it concise and platform-appropriate (280 chars for Twitter, longer for Instagram/LinkedIn)."""
        )
        
        self.chain = self.prompt | self.llm
    
    def create_caption(self, trend: str, brand_voice: str, platform: str, feedback: str = "") -> str:
        """Create a social media caption."""
        print_agent_message("Content Creator Agent", "Writing caption...", Fore.BLUE)
        
        feedback_text = f"Brand Guardian Feedback:\n{feedback}\nPlease revise accordingly." if feedback else ""
        
        caption = self.chain.invoke({
            "trend": trend,
            "brand_voice": brand_voice,
            "platform": platform,
            "feedback": feedback_text if feedback_text else "First draft - no feedback yet."
        })
        
        print_agent_message("Content Creator Agent", f"Caption:\n{caption}", Fore.BLUE)
        return caption


class ImageDescriberAgent:
    """Describes what image should be created (simulates image generation)."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_CREATIVE
        )
        
        self.prompt = PromptTemplate(
            input_variables=["caption", "trend"],
            template="""You are an AI Image Prompt Expert for DALL-E/Midjourney.

Social Media Caption:
{caption}

Trend/Topic: {trend}

Create a detailed image generation prompt that:
1. Visually represents the caption and trend
2. Specifies style (photo, illustration, 3D, etc.)
3. Includes composition details
4. Mentions colors and mood
5. Is optimized for social media (eye-catching, clear)

Provide ONLY the image prompt, ready to use."""
        )
        
        self.chain = self.prompt | self.llm
    
    def describe_image(self, caption: str, trend: str) -> str:
        """Create an image generation prompt."""
        print_agent_message("Image Describer Agent", "Creating image prompt...", Fore.YELLOW)
        
        image_prompt = self.chain.invoke({"caption": caption, "trend": trend})
        
        print_agent_message("Image Describer Agent", 
                          f"Image prompt:\n{image_prompt}\n\n[In production, this would be sent to DALL-E/Midjourney]", 
                          Fore.YELLOW)
        return image_prompt


class BrandGuardianAgent:
    """Ensures brand consistency and appropriateness."""
    
    def __init__(self, brand_guidelines: dict):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_ANALYTICAL
        )
        
        self.brand_guidelines = brand_guidelines
        
        self.prompt = PromptTemplate(
            input_variables=["caption", "guidelines"],
            template="""You are a Brand Compliance Officer.

Brand Guidelines:
{guidelines}

Proposed Social Media Post:
{caption}

Review the post for:
1. Brand voice alignment
2. Tone consistency
3. Prohibited words/phrases
4. Message clarity
5. Brand values alignment

If compliant, respond with "APPROVED: [brief reason]"
If not compliant, respond with "REJECTED: [specific issues and suggestions]" """
        )
        
        self.chain = self.prompt | self.llm
    
    def review_content(self, caption: str) -> tuple[bool, str]:
        """Review content for brand compliance."""
        print_agent_message("Brand Guardian Agent", "Reviewing for brand compliance...", Fore.CYAN)
        
        guidelines_text = "\n".join(f"- {k}: {v}" for k, v in self.brand_guidelines.items())
        
        review = self.chain.invoke({"caption": caption, "guidelines": guidelines_text})
        
        approved = "APPROVED" in review.upper()
        
        print_agent_message("Brand Guardian Agent", f"Review: {review}", Fore.CYAN)
        return approved, review


class SchedulerAgent:
    """Determines optimal posting time."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_ANALYTICAL
        )
        
        self.prompt = PromptTemplate(
            input_variables=["platform", "target_audience", "current_time"],
            template="""You are a Social Media Scheduling Expert.

Platform: {platform}
Target Audience: {target_audience}
Current Time: {current_time}

Recommend the optimal posting time considering:
1. Platform-specific peak engagement times
2. Target audience timezone and habits
3. Day of week
4. Content type best practices

Provide:
1. Recommended posting time (specific hour)
2. Reasoning
3. Alternative time if primary slot is not available"""
        )
        
        self.chain = self.prompt | self.llm
    
    def schedule_post(self, platform: str, target_audience: str) -> str:
        """Determine optimal posting time."""
        print_agent_message("Scheduler Agent", "Calculating optimal posting time...", Fore.GREEN)
        
        current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        
        schedule = self.chain.invoke({
            "platform": platform,
            "target_audience": target_audience,
            "current_time": current_time
        })
        
        print_agent_message("Scheduler Agent", f"Schedule recommendation:\n{schedule}", Fore.GREEN)
        return schedule


class SocialMediaManager:
    """Orchestrates the autonomous social media management system."""
    
    def __init__(self, brand_guidelines: dict):
        self.trend_monitor = TrendMonitorAgent()
        self.content_creator = ContentCreatorAgent()
        self.image_describer = ImageDescriberAgent()
        self.brand_guardian = BrandGuardianAgent(brand_guidelines)
        self.scheduler = SchedulerAgent()
    
    def create_post(self, industry: str, brand_voice: str, platform: str, target_audience: str, max_iterations: int = 2):
        """Create a complete social media post."""
        print_section("Autonomous Social Media Manager Started")
        
        # Step 1: Monitor trends
        trends = self.trend_monitor.find_trends(industry)
        
        # Select first trend (in production, could be more sophisticated)
        selected_trend = trends.split('\n')[0] if trends else "General industry topic"
        
        # Step 2: Create content with brand review loop
        approved = False
        feedback = ""
        iteration = 0
        
        while not approved and iteration < max_iterations:
            iteration += 1
            print_section(f"Content Creation Iteration {iteration}")
            
            # Create caption
            caption = self.content_creator.create_caption(selected_trend, brand_voice, platform, feedback)
            
            # Brand review
            approved, review = self.brand_guardian.review_content(caption)
            
            if not approved:
                feedback = review
            else:
                break
        
        if not approved:
            print_section("⚠ Content not approved after max iterations")
            return None
        
        # Step 3: Create image description
        image_prompt = self.image_describer.describe_image(caption, selected_trend)
        
        # Step 4: Schedule post
        schedule = self.scheduler.schedule_post(platform, target_audience)
        
        # Final output
        print_section("✓ Social Media Post Ready!")
        
        post_summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL POST PACKAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Platform: {platform}
📊 Trend: {selected_trend}

📝 Caption:
{caption}

🎨 Image Prompt:
{image_prompt}

📅 Recommended Schedule:
{schedule}

✅ Status: Approved for posting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(post_summary)
        
        return {
            "caption": caption,
            "image_prompt": image_prompt,
            "schedule": schedule,
            "trend": selected_trend
        }


def main():
    """Run the social media manager example."""
    
    # Define brand guidelines
    brand_guidelines = {
        "Voice": "Professional yet friendly, innovative",
        "Tone": "Positive, empowering, educational",
        "Prohibited": "No negative language, no competitor mentions",
        "Values": "Innovation, sustainability, community"
    }
    
    # Create manager
    manager = SocialMediaManager(brand_guidelines)
    
    # Create a post
    manager.create_post(
        industry="Technology Startups",
        brand_voice="Innovative and inspiring",
        platform="LinkedIn",
        target_audience="Tech professionals and entrepreneurs, ages 25-45",
        max_iterations=2
    )


if __name__ == "__main__":
    main()
