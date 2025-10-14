// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "SnapshotCaptureBlueprintLibrary.generated.h"

/**
 * 
 */
UCLASS()
class MYPROJECT2_API USnapshotCaptureBlueprintLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
    /**
     * Capture the current frame (viewport) and save it as a PNG or JPG file at the specified path.
     * @param FilePath - Full absolute path including filename and extension (.png or .jpg).
     * @param bShowUI - Whether UI elements should be included in the screenshot.
     * @return true if the request was accepted.
     */
    UFUNCTION(BlueprintCallable, Category = "FrameCapture")
    static bool CaptureCurrentFrameToFile(const FString& FilePath, bool bShowUI = false);
	
};
