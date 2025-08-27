import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.net.*;
import java.io.*;

public class BotApiTest {
    @Test
    public void testBotTokenValid() throws Exception {
        String botToken = System.getenv("BOT_TOKEN");
        assertNotNull(botToken, "BOT_TOKEN не найден в окружении!");

        URL url = new URL("https://api.telegram.org/bot" + botToken + "/getMe");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int responseCode = conn.getResponseCode();
        assertEquals(200, responseCode, "Telegram API не отвечает корректно!");
    }
}
