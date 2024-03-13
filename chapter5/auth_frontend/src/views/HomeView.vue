<template>
  <div>Home</div>
</template>

<script setup>
import { onMounted } from "vue";
import tryMakeHttpRequest from "@/tryMakeHttpRequest";

onMounted(async () => {
  try {
    const response = await tryMakeHttpRequest(
      "http://localhost:8000/api/messaging-service/messages",
      {
        method: "POST",
      },
    );

    console.log(
      `Message creation response status: ${response.status} ${response.statusText}`,
    );
  } catch (error) {
    console.log("Message creation request failed");
    console.log(error);
  }
});
</script>
