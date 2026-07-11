<template>
    <h2>Redirecting...</h2>
    <p>Если вы не были перенаправлены автоматически, <a href="https://discord.gg/sNxyV3ZpF">нажмите здесь</a>.</p>
</template>

<script>
    setTimeout(() => {
        console.log("Redirecting...");
        window.location.replace("https://discord.gg/sNxyV3ZpF");
    }, 500);
</script>