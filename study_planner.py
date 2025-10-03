import math
from tabulate import tabulate 
class StudyPlanner:
    def __init__(self):
        self.total_study_time = 0
        self.subjects = {}
        self.schedule = []
        self.difficulty_weights = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }

    def get_user_input(self):
        """
        Gathers study time, subjects, and their difficulty levels from the user.
        """
        print("🌟 Welcome to your Smart Study Planner! 🌟")
        print("Let's organize your time to achieve your goals brilliantly! ✨")

        while True:
            try:
                user_input = input("📚 How many hours do you have available for study today? (e.g., 4.5 or 4,5): ").strip().replace(',', '.')
                self.total_study_time = float(user_input)
                if self.total_study_time <= 0:
                    raise ValueError("Study time must be a positive number.")
                break
            except ValueError as e:
                print(f"🚫 Invalid input. Please enter a positive number for available study hours. Make sure to use a dot (.) for decimals if needed. Error: {e}")


        print("\n📝 Now, tell me about the subjects you want to study and their difficulty levels.")
        print("Type 'done' when you have finished adding all subjects.")

        while True:
            subject_name = input(f"📖 Enter subject name (or 'done' to finish): ").strip()
            if subject_name.lower() == 'done':
                if not self.subjects:
                    print("⚠️ You must add at least one subject to start planning!")
                    continue
                break

            while True:
                difficulty = input(f"💡 What is the difficulty for '{subject_name}'? (easy, medium, hard): ").lower().strip()
                
                if difficulty in self.difficulty_weights:
                    self.subjects[subject_name] = difficulty
                    print(f"✅ Successfully added '{subject_name}' with '{difficulty}' difficulty.")
                    break
                else:
                    print("❌ Invalid difficulty. Please choose from 'easy', 'medium', 'hard'.")

    def calculate_time_distribution(self):
        """
        Calculates how much time each subject gets based on its difficulty.
        """
        if not self.subjects:
            print("No subjects defined for study yet.")
            return {}

        total_weight = sum(self.difficulty_weights[diff] for diff in self.subjects.values())
        total_study_minutes = self.total_study_time * 60

        subject_study_minutes = {}
        for subject, difficulty in self.subjects.items():
            weight = self.difficulty_weights[difficulty]
            subject_study_minutes[subject] = (weight / total_weight) * total_study_minutes

        return subject_study_minutes

    def generate_schedule(self):
        """
        Generates a detailed daily study schedule with breaks.
        """
        self.schedule = []
        subject_times = self.calculate_time_distribution()
        
        if not subject_times:
            return

        current_time_minutes = 0
        
        remaining_subject_time = {s: t for s, t in subject_times.items()}

        while any(time > 0 for time in remaining_subject_time.values()):
            scheduled_block_found = False
            
            available_subjects = [(s, t) for s, t in remaining_subject_time.items() if t > 0]
            if not available_subjects:
                break 

            available_subjects.sort(key=lambda x: x[1], reverse=True)
            
            current_subject_to_schedule = available_subjects[0][0] 
            
            block_duration = min(60, remaining_subject_time[current_subject_to_schedule])
            
            if len(self.schedule) > 0: 
                last_item_was_study = False
                temp_study_counter = 0
                for item_in_schedule in reversed(self.schedule):
                    if "Break" in item_in_schedule:
                        break 
                    else:
                        parts = item_in_schedule.split(': ')
                        if len(parts) > 1:
                            duration_str = parts[1].replace(' minutes', '').replace(')', '').strip()
                            try:
                                temp_study_counter += int(duration_str)
                                last_item_was_study = True
                            except ValueError:
                                pass 

                if last_item_was_study and temp_study_counter >= 60:
                    self.schedule.append(f"Quick Break ☕ (10 minutes)")
                    current_time_minutes += 10 
            
            self.schedule.append(f"{current_subject_to_schedule}: {int(block_duration)} minutes")
            current_time_minutes += block_duration
            remaining_subject_time[current_subject_to_schedule] -= block_duration
            scheduled_block_found = True
            
            if not scheduled_block_found:
                break 


    def display_schedule(self):
        """
        Prints the generated daily study schedule in a clear and creative format using a table.
        """
        if not self.schedule:
            print("😔 We couldn't create a study schedule. Did you enter your subjects correctly?")
            return

        print("\n\n✨🚀 Your Inspiring Study Schedule for a Great Day! 🚀✨")
        print("------------------------------------------")
        
        table_data = []
        current_minute = 0
        
        headers = ["Start Time ⏰", "Activity 📚", "Duration (min) ⏱️", "Motivation ✨"]

        for item in self.schedule:
            hours = current_minute // 60
            minutes = current_minute % 60
            start_time = f"{int(hours):02d}:{int(minutes):02d}"

            if "Break" in item:
                duration = 10
                activity = "Break ☕"
                motivation = "Relax and get ready to launch again! 🌈"
                table_data.append([start_time, activity, duration, motivation])
            else:
                parts = item.split(': ')
                subject_name = parts[0]
                duration = int(parts[1].replace(' minutes', ''))
                
                emoji = "📖" 
                motivation_text = "Focus and create! 💪"
                if self.subjects.get(subject_name) == 'hard':
                    emoji = "🧠" 
                    motivation_text = "Tackle the challenge! You've got this! 💥"
                elif self.subjects.get(subject_name) == 'medium':
                    emoji = "💡" 
                    motivation_text = "Explore and understand! New insights await! 🤔"
                elif self.subjects.get(subject_name) == 'easy':
                    emoji = "✅" 
                    motivation_text = "Master the basics! Build a strong foundation! 🌱"

                activity = f"{emoji} {subject_name}"
                table_data.append([start_time, activity, duration, motivation_text])
            
            current_minute += duration
        
        final_hours = current_minute // 60
        final_minutes = current_minute % 60
        final_time = f"{int(final_hours):02d}:{int(final_minutes):02d}"
        
        # Print the table
        print(tabulate(table_data, headers=headers, tablefmt="grid")) # "grid" for a nice framed table

        print("------------------------------------------")
        print(f"🎉 Your amazing study schedule ends at approximately {final_time}! Keep up the great work! ⭐")

# Main execution
if __name__ == "__main__":
    planner = StudyPlanner()
    planner.get_user_input()
    planner.generate_schedule()
    planner.display_schedule()