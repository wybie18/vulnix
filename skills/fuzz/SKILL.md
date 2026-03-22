---
name: fuzz
description: 'Strict fuzzing methodology for generating harnesses, structuring mutation schemas, and conducting deep crash triage. Use for analyzing unhandled exceptions in APIs and binary memory corruptions.'
---

# Fuzz Testing & Crash Analysis Skill

This skill enforces a methodical approach to Fuzz Testing. It provides structured guidance on how to generate fuzzing harnesses, seed corpuses properly to achieve deep code coverage, and triage the resulting crashes safely and accurately.

## When to Activate
• Building fuzzing harnesses for arbitrary binary formats, REST APIs, or system software (AFL++, libFuzzer).
• Defining structure-aware mutation strategies for complex inputs (GraphQL, JSON, XML).
• Analyzing and triaging crash logs (AddressSanitizer/ASAN, MSAN, Valgrind).
• Determining if a crash is a functional bug (e.g., divide by zero) or a security vulnerability (e.g., Use-After-Free, Heap Buffer Overflow).

## Fuzzing Methodology Checklist

### 1. Harness Generation & Target Scoping
A fuzzer is only as good as its harness.

#### ❌ NEVER Accept This
- Fuzzing an entire massive application entry point via network sockets if an internal parsing library can be fuzzed directly in-memory.
- Harnesses that do not reset state between iterations (leading to false crashes from un-flushed memory).

#### ✅ ALWAYS Verify This
- Target the specific input parser, isolated from standard networking overhead where possible.
- Ensure the harness resets global/static variables if the fuzzing engine runs entirely in-memory (e.g., `LLVMFuzzerTestOneInput`).

#### Verification Steps
- [ ] Harness targets the lowest-level parsing function possible.
- [ ] State is cleanly cleared at the end of every fuzzer loop.
- [ ] Target compiled with AddressSanitizer (`-fsanitize=address`).

### 2. Seed Generation & Corpus Selection
Coverage relies on high-quality initial seeds.

#### ❌ NEVER Do This
- Start a mutational fuzzer with only the letter "A" when fuzzing a strictly formatted protocol like a PDF or JSON payload.
- Include massive, multi-megabyte files in the initial seed corpus (wastes CPU cycles).

#### ✅ ALWAYS Do This
- Extract minimal, valid, completely covered file formats to start the corpus.
- Load defined formats for structural fuzzing:
   - [JSON Seeds](./seeds/json_seeds.txt)
   - [XML Seeds](./seeds/xml_seeds.txt)
   - [Binary Seeds](./seeds/binary_seeds.txt)

#### Verification Steps
- [ ] Corpus size minimized (files optimally < 1KB if possible).
- [ ] Standard schemas provided to structure-aware fuzzers (like protobufs or grammar dictionaries).

### 3. Crash Triage & Security Classification
Not all unhandled exceptions are security flaws.

#### ❌ NEVER Accept This
- Classifying an intentional runtime assertions/aborts (e.g., `assert(x != NULL)`) securely stopping a program as a "Remote Code Execution" vulnerability.
- Reporting "Denial of Service" via CPU exhaustion on a local CLI tool that isn't exposed to the network.

#### ✅ ALWAYS Do This
- Read the ASAN trace to identify the exact memory violation:
  - `heap-buffer-overflow` / `stack-buffer-overflow` -> Potential RCE.
  - `use-after-free` -> High Potential RCE.
  - `SEGV on unknown address 0x000000000000` -> (Null Pointer Dereference) functionally annoying, rarely exploitable.
- Minimize the crashing test case specifically to the bytes that trigger the crash before reporting.

#### Verification Steps
- [ ] The crashing input reproduces the crash deterministically.
- [ ] ASAN/Valgrind stack trace definitively confirms the flaw category.
- [ ] Security boundaries evaluated (is this code accessible to an untrusted user?).

---

## Output Parsing & Handoff
When handing findings off to the `exploit` or `report` agents, ensure you provide:
1. The **Crashing Payload** (hex-encoded if binary).
2. The **Harness Code** utilized.
3. The **Sanitizer Stack Trace** pointing to the exact line in the source code causing the memory violation.
