# Exercise GIF Library

Visual exercise guide with GIFs and instructions for pickleball warmup and training.

## Features

- 🎬 GIF animations for each exercise
- 📝 Bilingual instructions (English + 中文)
- 🏷️ Category filtering (Warmup, Lower Body, Upper Body, Core, Mobility, Sport-Specific)
- 🔍 Search functionality
- 📱 Mobile responsive

## Pickleball Warmup Routine (20-30 mins)

1. **Warmup (3 min)** - High knees, arm circles, bodyweight squats
2. **Lower Body (7 min)** - Lateral lunges, single-leg RDL, calf raises, split squats
3. **Upper Body (8 min)** - Lat pulldown, cable woodchoppers, push-ups, shoulder press
4. **Mobility (7 min)** - Side leg swings, torso twists
5. **Sport-Specific (5 min)** - Shadow swings, split-step practice

## Deployment

Push to GitHub → Zeabur auto-deploys at https://gameworld.zeabur.app/exercise-gif-library/

## Adding New Exercises

Edit `index.html` and add to the `exercises` array:

```javascript
{
    id: 16,
    name: "Exercise Name",
    nameCn: "中文名稱",
    emoji: "🦵",
    category: "lower", // warmup|lower|upper|core|mobility|sport
    muscleGroup: "Target muscles",
    gifUrl: "https://media.giphy.com/...",
    instructions: ["Step 1", "Step 2", ...],
    reps: "10-12 reps",
    videoUrl: "https://youtube.com/..."
}
```
