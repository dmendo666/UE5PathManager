// Fill out your copyright notice in the Description page of Project Settings.


#include "SnapshotCaptureBlueprintLibrary.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "UnrealClient.h" // For FScreenshotRequest

bool USnapshotCaptureBlueprintLibrary::CaptureCurrentFrameToFile(const FString& FilePath, bool bShowUI)
{
    if (!GEngine || !GEngine->GameViewport)
    {
        UE_LOG(LogTemp, Warning, TEXT("CaptureCurrentFrameToFile: No valid GameViewport found."));
        return false;
    }

    // Request the screenshot to be saved to given path - async operation internally
    FScreenshotRequest::RequestScreenshot(FilePath, bShowUI, false);

    UE_LOG(LogTemp, Log, TEXT("Screenshot requested: %s"), *FilePath);
    return true;
}

