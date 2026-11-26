import AppKit
import Security

enum ClipboardCopyError: Error {
    case lookup(OSStatus)
    case unexpectedReferences
    case ambiguousSelection
    case invalidText
    case clipboardWriteFailed
}

func copyKeychainPassword(
    account: String,
    service: String,
    match: (CFDictionary, UnsafeMutablePointer<CFTypeRef?>?) -> OSStatus = SecItemCopyMatching,
    write: (Data) -> Bool
) throws {
    let referenceQuery = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrAccount: account,
        kSecAttrService: service,
        kSecReturnPersistentRef: true,
        kSecMatchLimit: kSecMatchLimitAll,
    ] as CFDictionary

    var result: CFTypeRef?
    let referenceStatus = match(referenceQuery, &result)
    guard referenceStatus == errSecSuccess else { throw ClipboardCopyError.lookup(referenceStatus) }
    guard let references = result as? [Data], !references.isEmpty else {
        throw ClipboardCopyError.unexpectedReferences
    }
    guard references.count == 1 else { throw ClipboardCopyError.ambiguousSelection }

    // Bind the read to the item we resolved instead of repeating the name search.
    let passwordQuery = [
        kSecClass: kSecClassGenericPassword,
        kSecAttrAccount: account,
        kSecAttrService: service,
        kSecMatchItemList: references,
        kSecReturnData: true,
    ] as CFDictionary
    result = nil
    let passwordStatus = match(passwordQuery, &result)
    guard passwordStatus == errSecSuccess else { throw ClipboardCopyError.lookup(passwordStatus) }
    guard let data = result as? Data, String(data: data, encoding: .utf8) != nil else {
        throw ClipboardCopyError.invalidText
    }
    guard write(data) else { throw ClipboardCopyError.clipboardWriteFailed }
}

func writeClipboardText(_ data: Data, to pasteboard: NSPasteboard) -> Bool {
    pasteboard.prepareForNewContents(with: .currentHostOnly)
    return pasteboard.setData(data, forType: .string)
}

#if !MANAGE_SECRET_TEST
let arguments = CommandLine.arguments
guard arguments.count == 3, !arguments[1].isEmpty, !arguments[2].isEmpty else {
    FileHandle.standardError.write(Data("Usage: copy-keychain-password.swift <account> <service>\n".utf8))
    exit(2)
}

do {
    try copyKeychainPassword(account: arguments[1], service: arguments[2]) {
        writeClipboardText($0, to: .general)
    }
} catch {
    let message: String
    switch error {
    case ClipboardCopyError.lookup(let status):
        message = "Keychain lookup failed (OSStatus \(status))."
    case ClipboardCopyError.unexpectedReferences:
        message = "Could not identify a matching Keychain entry."
    case ClipboardCopyError.ambiguousSelection:
        message = "Multiple Keychain entries match this service and account. Choose the intended entry in Keychain Access."
    case ClipboardCopyError.invalidText:
        message = "The Keychain item could not be read as UTF-8 text."
    default:
        message = "Could not write to the macOS clipboard."
    }
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(1)
}
#endif
