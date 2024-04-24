import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Toast
import androidx.fragment.app.Fragment
import io.github.privacystreams.ChainStreamClient.ChainStreamClientService
import io.github.privacystreams.ChainStreamClient.LogReaderTask
import io.github.privacystreams.ChainStreamClient.R

class HomePageFragment : Fragment() {

    private var isServerRunning: Boolean = false
    private lateinit var logReaderTask: LogReaderTask

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.activity_main, container, false)

        val buttonStart = view.findViewById<Button>(R.id.button)
        val buttonStop = view.findViewById<Button>(R.id.button2)
        val logLinearLayout = view.findViewById<LinearLayout>(R.id.logLinearLayout)
        val logScrollView = view.findViewById<ScrollView>(R.id.logScrollView)
        val buttonClear = view.findViewById<Button>(R.id.button3)

        logReaderTask = LogReaderTask(logLinearLayout, requireActivity(), logScrollView)

        buttonStart.setOnClickListener { view ->
            if (!isServerRunning) {
                logReaderTask.startReadingLogs()

                val intent = Intent(requireActivity(), ChainStreamClientService::class.java)
                requireActivity().startService(intent)

                isServerRunning = true
                Toast.makeText(view.context, "server running!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(view.context, "server already running!", Toast.LENGTH_SHORT).show()
            }
        }

        buttonStop.setOnClickListener { view ->
            if (isServerRunning) {
                val intent = Intent(requireActivity(), ChainStreamClientService::class.java)
                requireActivity().stopService(intent)

                isServerRunning = false
                Toast.makeText(view.context, "server stop!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(view.context, "server not running!", Toast.LENGTH_SHORT).show()
            }
        }

        buttonClear.setOnClickListener { logLinearLayout.removeAllViews() }

        return view
    }
}
