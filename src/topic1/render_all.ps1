# Render all Topic 1 scenes
# Usage: Run from src/ directory
# Quality flags: -ql (low/480p), -qm (medium/720p), -qh (high/1080p), -qk (4K)

$quality = "-qm"  # Match manim.cfg medium_quality
$scenes = @(
    @{ File = "topic1/scene_01_hook.py";                        Class = "Scene01Hook" },
    @{ File = "topic1/scene_02_limited_agents.py";              Class = "Scene02LimitedAgents" },
    @{ File = "topic1/scene_03_recipe.py";                      Class = "Scene03Recipe" },
    @{ File = "topic1/scene_04_open_ended.py";                  Class = "Scene04OpenEnded" },
    @{ File = "topic1/scene_05_prediction_vs_interaction.py";   Class = "Scene05PredictionVsInteraction" },
    @{ File = "topic1/scene_06_genie1.py";                      Class = "Scene06Genie1" },
    @{ File = "topic1/scene_07_latent_actions.py";              Class = "Scene07LatentActions" },
    @{ File = "topic1/scene_08_playable_world.py";              Class = "Scene08PlayableWorld" },
    @{ File = "topic1/scene_09_genie2.py";                      Class = "Scene09Genie2" },
    @{ File = "topic1/scene_10_realtime_caveat.py";             Class = "Scene10RealtimeCaveat" },
    @{ File = "topic1/scene_11_physics.py";                     Class = "Scene11Physics" },
    @{ File = "topic1/scene_12_sima.py";                        Class = "Scene12SIMA" },
    @{ File = "topic1/scene_13_bigger_vision.py";               Class = "Scene13BiggerVision" },
    @{ File = "topic1/scene_14_ending.py";                      Class = "Scene14Ending" }
)

$total = $scenes.Count
$success = 0
$failed = @()

Write-Host "`n=== Rendering Topic 1: $total scenes ===" -ForegroundColor Cyan
Write-Host ""

foreach ($i in 0..($total - 1)) {
    $scene = $scenes[$i]
    $num = $i + 1
    Write-Host "[$num/$total] Rendering $($scene.Class)..." -ForegroundColor Yellow

    $cmd = "manim $quality $($scene.File) $($scene.Class)"
    Write-Host "  > $cmd" -ForegroundColor DarkGray

    try {
        Invoke-Expression $cmd
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK" -ForegroundColor Green
            $success++
        } else {
            Write-Host "  FAILED (exit code $LASTEXITCODE)" -ForegroundColor Red
            $failed += $scene.Class
        }
    } catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
        $failed += $scene.Class
    }

    Write-Host ""
}

Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "  Success: $success / $total" -ForegroundColor Green

if ($failed.Count -gt 0) {
    Write-Host "  Failed:" -ForegroundColor Red
    foreach ($f in $failed) {
        Write-Host "    - $f" -ForegroundColor Red
    }
}

Write-Host "`nOutput: ./media/videos/" -ForegroundColor DarkGray
