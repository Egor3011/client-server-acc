<template>
    <h2>Redirecting...</h2>
    <p>Если вы не были перенаправлены автоматически, <a href="https://discord.gg/zEApGt3pgx">нажмите здесь</a>.</p>
</template>

<script>
    setTimeout(() => {
        console.log("Redirecting...");
        window.location.replace("https://discord.gg/zEApGt3pgx");
    }, 500);
</script>